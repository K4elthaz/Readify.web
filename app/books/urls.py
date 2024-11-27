from django.urls import path

from app.books.views.services import (
    save_new_book_service,
    save_new_content_service,
    next_chapter_service,
    previous_chapter_service,
    remove_chapter_service,
    delete_book_service,
    publish_book_service,
    add_to_favorites,
    delete_from_favorites,
    follow_author_service,
    search_service,
    update_book_content_service,
    search_collab_service,
    invite_collaborator,
    refresh_plagiarism_reports,
    write_a_review,
    respond_to_invitations,
    update_book_service,
    unpublish_book_service,
)
from app.books.views.views import (
    MyLibraryView,
    BookDetail,
    WriteBookContent,
    BookContentDetail,
    BrowseBooksView,
    MyFavoritesView,
    UpdateBookContentView,
    PlagiarismCheckerTableResult,
)

service_urlpatterns = [
    path("books/save/new", save_new_book_service, name="save_new_book_service"),
    path(
        "books/content/save/new/<str:slug>",
        save_new_content_service,
        name="save_new_content_service",
    ),
    path(
        "books/content/next-chapter/<str:slug>",
        next_chapter_service,
        name="next_chapter_service",
    ),
    path(
        "books/content/previous-chapter/<str:slug>",
        previous_chapter_service,
        name="previous_chapter_service",
    ),
    path(
        "books/content/remove-chapter/<str:book_slug>/<str:chapter_slug>",
        remove_chapter_service,
        name="remove_chapter_service",
    ),
    path(
        "books/delete/<str:slug>",
        delete_book_service,
        name="delete_book_service",
    ),
    path(
        "books/publish/<str:slug>",
        publish_book_service,
        name="publish_book_service",
    ),
    path(
        "books/unpublish/<str:slug>",
        unpublish_book_service,
        name="unpublish_book_service",
    ),
    path(
        "books/add-to-favorites/<str:slug>",
        add_to_favorites,
        name="add_to_favorites",
    ),
    path(
        "books/delete-from-favorites/<str:slug>",
        delete_from_favorites,
        name="delete_from_favorites",
    ),
    path(
        "books/author/follow/<str:author_id>/",
        follow_author_service,
        name="follow_author_service_v2",
    ),
    path(
        "search/",
        search_service,
        name="search_service",
    ),
    path(
        "book/content/update/<str:slug>/",
        update_book_content_service,
        name="update_book_content_service",
    ),
    path(
        "collab/search/<str:slug>/",
        search_collab_service,
        name="search_collab_service",
    ),
    path(
        "collab/invite/<str:slug>/",
        invite_collaborator,
        name="invite_collaborator",
    ),
    path(
        "plagiarism/refresh/<str:slug>/",
        refresh_plagiarism_reports,
        name="refresh_plagiarism_reports",
    ),
    path(
        "review/write/<str:slug>/",
        write_a_review,
        name="write_a_review",
    ),
    path(
        "collaborations/respond/<str:book_slug>/<str:status>/<str:id>/",
        respond_to_invitations,
        name="respond_to_invitations",
    ),
    path(
        "book/update/<str:slug>/",
        update_book_service,
        name="update_book_service",
    ),
]
urlpatterns = [
    path("books/library", MyLibraryView.as_view(), name="book_library"),
    path("book/detail/<str:slug>", BookDetail.as_view(), name="book_detail"),
    path(
        "book/content/write/<str:slug>",
        WriteBookContent.as_view(),
        name="write_book_content",
    ),
    path(
        "book/content/detail/<str:slug>",
        BookContentDetail.as_view(),
        name="book_content_detail",
    ),
    path(
        "books/browse",
        BrowseBooksView.as_view(),
        name="browse_books",
    ),
    path(
        "books/favorites",
        MyFavoritesView.as_view(),
        name="my_favorites",
    ),
    path(
        "books/content/update/<str:slug>",
        UpdateBookContentView.as_view(),
        name="update_book_content",
    ),
    path(
        "books/plagiarism/<str:slug>",
        PlagiarismCheckerTableResult.as_view(),
        name="plagiarism_checker_table",
    ),
] + service_urlpatterns
