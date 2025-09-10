"""Integration tests hitting endpoints using httpx.AsyncClient and pytest-asyncio."""
import pytest

pytestmark = pytest.mark.asyncio


async def test_create_book(client):
    payload = {"title": "Async Test Book", "description": "A test book."}
    resp = await client.post("/books/", json=payload)

    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert "id" in data


async def test_list_books(client):
    # First, create a book
    payload = {"title": "Another Book", "description": "Listed book."}
    create_resp = await client.post("/books/", json=payload)
    assert create_resp.status_code == 201

    # Then, list all books
    list_resp = await client.get("/books/")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert isinstance(items, list)
    assert any(b["title"] == payload["title"] for b in items)


async def test_get_book(client):
    # Create a book
    payload = {"title": "Single Book", "description": "For fetching"}
    create_resp = await client.post("/books/", json=payload)
    book_id = create_resp.json()["id"]

    # Fetch by ID
    get_resp = await client.get(f"/books/{book_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == book_id
    assert data["title"] == payload["title"]


async def test_update_book(client):
    # Create book
    payload = {"title": "Old Title", "description": "Old description"}
    create_resp = await client.post("/books/", json=payload)
    book_id = create_resp.json()["id"]

    # Update book
    update_payload = {"title": "New Title", "description": "New description"}
    update_resp = await client.put(f"/books/{book_id}", json=update_payload)

    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["title"] == "New Title"
    assert updated["description"] == "New description"


async def test_delete_book(client):
    # Create book
    payload = {"title": "Delete Me", "description": "Temporary"}
    create_resp = await client.post("/books/", json=payload)
    book_id = create_resp.json()["id"]

    # Delete book
    del_resp = await client.delete(f"/books/{book_id}")
    assert del_resp.status_code == 204

    # Verify deletion
    get_resp = await client.get(f"/books/{book_id}")
    assert get_resp.status_code == 404
