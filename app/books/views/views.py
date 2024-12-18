import asyncio
import pprint

from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from app.authentication.models import User, FollowedAuthor
from app.books.forms import BookForm, BookContentForm
from app.books.models import (
    Books,
    BooksChapter,
    ChapterUnlockedByUser,
    ProofOfPaymentByUser,
    UsersFavorites,
    PlagiarismCheckerLogs,
    Rates,
)
from app.rewards.models import Rewards, ClaimedRewards
from app.utils import plagiarism_checker, natural_time
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

# Create your views here.
class MyLibraryView(LoginRequiredMixin, ListView):
    template_name = "book_library.html"
    login_url = "/signin"
    model = Books
    context_object_name = "books"

    def get_queryset(self):
        # Filter to get books authored or co-authored by the current user
        queryset = (
            super()
            .get_queryset()
            .filter(Q(author=self.request.user) | Q(co_authors=self.request.user))
            .distinct()  # Ensure distinct books are returned
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_library_active"] = True
        context["form"] = BookForm()
        context["page_title"] = "My Library"
        context["page_description"] = (
            "View all the books you've created, including both published and draft books."
        )

        return context


class BookDetail(LoginRequiredMixin, DetailView):
    template_name = "book_detail.html"
    login_url = "/signin"
    context_object_name = "book"  # More appropriate context object name
    model = Books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        user = self.request.user

        chapters = BooksChapter.objects.filter(
            book__slug=slug, is_archived=False
        ).order_by("chapter_number")

        rates = Rates.objects.filter(book__slug=slug).order_by("-created_at")

        chapters_list = [
            {
                "id": chapter.id,
                "title": chapter.title,
                "chapter_number": chapter.chapter_number,
                "is_locked": (
                    False
                    if ChapterUnlockedByUser.objects.filter(
                        paid_by=user, chapter_id=chapter.id
                    ).exists()
                    else chapter.is_locked
                ),
                "slug": chapter.slug,
                "created_at": natural_time(chapter.created_at),
                "updated_at": natural_time(chapter.updated_at),
                "images": chapter.images,
                "GcashPayments": ProofOfPaymentByUser.objects.filter(paid_by=user, chapter_id=chapter.id),
            }
            for chapter in chapters
        ]

        is_co_authored = Books.objects.filter(
            slug=slug, co_authors=self.request.user
        ).exists()
        context["book_library_active"] = True
        context["chapters"] = chapters_list
        context["slug"] = slug
        context["user"] = user
        context["is_already_favorites"] = UsersFavorites.objects.filter(
            reader=user, book__slug=slug
        ).exists()
        context["is_co_authored"] = is_co_authored
        context["rates"] = rates
        context["rate_count"] = (
            rates.first().get_total_rates_per_book() if rates.exists() else 0
        )
        context["form"] = BookForm(self.request.POST or None, instance=self.object)
        return context


class WriteBookContent(LoginRequiredMixin, CreateView):
    template_name = "write_book_content.html"
    login_url = "/signin"
    form_class = BookContentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.kwargs["slug"]

        # Get the book object based on the slug
        book = Books.objects.filter(slug=self.kwargs["slug"]).first()

        # Check if a book exists
        if book:
            try:
                # Attempt to get the latest chapter
                current_chapter = (
                    BooksChapter.objects.only("chapter_number")
                    .filter(book=book, is_archived=False)
                    .latest("created_at")
                )
                context["current_chapter_number"] = current_chapter.chapter_number + 1
            except BooksChapter.DoesNotExist:
                # If no chapter exists, set the current chapter number to 1
                context["current_chapter_number"] = 1
        else:
            # Handle the case if the book itself does not exist
            context["current_chapter_number"] = None  # or another fallback value

        context["book_library_active"] = True

        return context


class BookContentDetail(LoginRequiredMixin, DetailView):
    template_name = "book_content_detail.html"
    login_url = "/signin"
    model = BooksChapter
    context_object_name = "content"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access the current object (the book chapter) using self.object
        content_object = self.object
        user = self.request.user
        context["slug"] = self.kwargs["slug"]
        context["book_library_active"] = True

        # check_plagiarism = self.run_plagiarism_check(content_object.content)
        return context


class BrowseBooksView(LoginRequiredMixin, ListView):
    template_name = "browse_books.html"
    login_url = "/signin"
    model = Books
    context_object_name = "books"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(is_published=True)
            .prefetch_related("user_libraries")
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        preferences = (
            user.onboarding[0].get("book_preferences", [])
            if user.onboarding and len(user.onboarding) > 0
            else []
        )

        today = timezone.now().date()

        rewards = Rewards.objects.filter(
            user=user,
            updated_at__date=today,
        )
        recommended_books = Books.objects.filter(
            category__name__in=preferences, is_published=True
        ).distinct()[:4]
        recommended_authors_queryset = User.objects.filter(user_role="writer")
        recommended_authors = [
            {
                "id": author.id,
                "full_name": author.full_name(),
                "username": author.username,
                "profile_picture": author.profile_picture,
                "num_of_authored_books": Books.objects.filter(
                    Q(author_id=author.id) & Q(is_published=True)
                ).count(),
                "is_already_followed": FollowedAuthor.objects.filter(
                    user=user, author_id=author.id
                ).exists(),
            }
            for author in recommended_authors_queryset
        ]

        all_payment_proof = ProofOfPaymentByUser.objects.all()

        pay_unlock = ChapterUnlockedByUser.objects.all()

        context["browse_books"] = True
        context["proof_of_payment"] = all_payment_proof
        context["pay_unlock"] = pay_unlock
        context["page_title"] = "Browse Books"
        context["page_description"] = "View all the published books available here."
        context["rewards"] = rewards.exists()
        context["recommended_books"] = recommended_books
        context["recommended_authors"] = recommended_authors
        return context


class MyFavoritesView(LoginRequiredMixin, ListView):
    template_name = "book_library.html"
    login_url = "/signin"
    model = Books
    context_object_name = "books"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(user_libraries__reader=self.request.user, is_published=True)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_library_active"] = True
        context["form"] = BookForm()
        context["page_title"] = "My Favorites"
        context["page_description"] = "View all your favorited books."

        return context


class UpdateBookContentView(LoginRequiredMixin, UpdateView):
    template_name = "update_book_content.html"
    login_url = "/signin"
    model = BooksChapter
    form_class = BookContentForm

    # Override get_success_url to dynamically include slug
    def get_success_url(self):
        return reverse_lazy("book_content_detail", kwargs={"slug": self.object.slug})

    # Pass the current chapter number and page description to the templates context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["content"] = self.object.content
        context["current_chapter_number"] = self.object.chapter_number
        context["slug"] = self.object.slug
        context["content_id"] = self.object.id
        return context


class PlagiarismCheckerTableResult(LoginRequiredMixin, DetailView):
    template_name = "book_plagiarism_table.html"
    login_url = "/signin"
    model = Books
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access the current object (the book chapter) using self.object
        content_object = self.object
        user = self.request.user
        slug = self.kwargs["slug"]

        book_id = content_object.id
        plagiarism_checker_logs = PlagiarismCheckerLogs.objects.filter(
            book=book_id
        ).order_by("-created_at")

        context["plagiarism_checker_logs"] = plagiarism_checker_logs

        return context

@method_decorator(csrf_exempt, name='dispatch')
class UpdateChapterStatusView(View):
    def post(self, request, *args, **kwargs):
        # Extract chapter ID from URL
        chapter_id = kwargs.get('id')  
        
        # Parse JSON body
        try:
            data = json.loads(request.body)
            action = data.get('action')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        # Validate action
        if action not in ['approve', 'decline']:
            return JsonResponse({"error": "Invalid action"}, status=400)

        # Get chapter and update status
        chapter_unlocked = get_object_or_404(ChapterUnlockedByUser, id=chapter_id)
        new_status = 'approved' if action == 'approve' else 'declined'
        chapter_unlocked.status = new_status
        chapter_unlocked.save()

        return JsonResponse({
            "message": "Status updated successfully",
            "status": chapter_unlocked.status
        })