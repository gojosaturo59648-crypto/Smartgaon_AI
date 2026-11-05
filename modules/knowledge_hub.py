
import streamlit as st
import sqlite3
import requests
from urllib.parse import quote_plus
from modules.ai import ask_groq

DB_NAME = "smartgaon.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            class_name TEXT,
            board TEXT,
            subject TEXT,
            medium TEXT,
            pdf_url TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def add_book(title, class_name, board, subject, medium, pdf_url):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT INTO knowledge_books
        (title, class_name, board, subject, medium, pdf_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, class_name, board, subject, medium, pdf_url))
    conn.commit()
    conn.close()


def get_local_books(search=""):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    if search.strip():
        term = f"%{search.strip()}%"
        rows = conn.execute("""
            SELECT * FROM knowledge_books
            WHERE title LIKE ? OR subject LIKE ?
            ORDER BY title
        """, (term, term)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM knowledge_books ORDER BY title
        """).fetchall()

    conn.close()
    return rows


def search_online_books(query, max_results=10):
    """Search Google Books public API. No API key required."""
    url = "https://www.googleapis.com/books/v1/volumes"

    try:
        response = requests.get(
            url,
            params={
                "q": query,
                "maxResults": max_results,
                "printType": "books"
            },
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        results = []

        for item in data.get("items", []):
            info = item.get("volumeInfo", {})

            title = info.get("title", "Untitled")
            authors = ", ".join(info.get("authors", ["Author not listed"]))
            publisher = info.get("publisher", "Publisher not listed")
            description = info.get("description", "")
            preview = info.get("previewLink")
            info_link = info.get("infoLink")
            thumbnail = info.get("imageLinks", {}).get("thumbnail")

            results.append({
                "title": title,
                "authors": authors,
                "publisher": publisher,
                "description": description,
                "preview": preview,
                "info_link": info_link,
                "thumbnail": thumbnail
            })

        return results, None

    except requests.exceptions.Timeout:
        return [], "Online search timed out. Please try again."
    except requests.exceptions.RequestException:
        return [], "Could not connect to Google Books. Check your internet connection."
    except Exception as e:
        return [], f"Search error: {e}"


def show_knowledge_hub():

    init_db()

    st.markdown("""
    <style>
    .stApp h1, .stApp h2, .stApp h3,
    .stApp p, .stApp label,
    .stApp span, .stApp li,
    .stApp [data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }

    .stApp input, .stApp textarea,
    .stApp [data-baseweb="select"] * {
        color: #ffffff !important;
    }

    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📚 Knowledge Hub")
    st.caption("Find books, explore knowledge and learn new things.")

    find_tab, add_tab, ai_tab, solve_tab = st.tabs([
        "🔎 Find Books",
        "➕ Add Book",
        "🤖 Knowledge AI",
        "📝 Solve Question"
    ])

    # ---------------- FIND BOOKS ----------------
    with find_tab:
        st.subheader("Find a Textbook")

        search_mode = st.radio(
            "Where should we search?",
            ["Online + My Library", "My Library Only"],
            horizontal=True
        )

        query = st.text_input(
            "Book name, subject or topic",
            placeholder="Example: Class 9 Science"
        )

        col1, col2 = st.columns(2)

        with col1:
            class_name = st.selectbox(
                "Class",
                ["Any Class"] + [f"Class {i}" for i in range(1, 13)]
            )

        with col2:
            board = st.selectbox(
                "Board",
                ["Any Board", "NCERT", "CBSE", "ICSE", "BSEB", "Other"]
            )

        if st.button("Search Books", type="primary"):
            if not query.strip():
                st.warning("Please enter a book name or subject.")
            else:
                search_text = query.strip()

                if class_name != "Any Class":
                    search_text += " " + class_name

                if board != "Any Board":
                    search_text += " " + board

                st.session_state["book_search_query"] = search_text
                st.session_state["book_search_mode"] = search_mode

        if st.session_state.get("book_search_query"):
            search_text = st.session_state["book_search_query"]
            mode = st.session_state.get("book_search_mode")

            st.markdown("### Your Library Results")

            local_books = get_local_books(query)

            if local_books:
                for book in local_books:
                    with st.expander(book["title"]):
                        st.write("Class:", book["class_name"] or "Not specified")
                        st.write("Board:", book["board"] or "Not specified")
                        st.write("Subject:", book["subject"] or "Not specified")
                        st.write("Medium:", book["medium"] or "Not specified")

                        if book["pdf_url"]:
                            st.markdown(
                                f"[Open saved book]({book['pdf_url']})"
                            )
            else:
                st.info("No matching book found in your saved library.")

            if mode == "Online + My Library":
                st.markdown("### 🌐 Online Book Results")

                with st.spinner("Searching online books..."):
                    results, error = search_online_books(search_text)

                if error:
                    st.warning(error)

                elif results:
                    for book in results:
                        with st.container(border=True):
                            st.markdown(f"#### {book['title']}")
                            st.write("Author:", book["authors"])
                            st.write("Publisher:", book["publisher"])

                            if book["thumbnail"]:
                                st.image(book["thumbnail"], width=100)

                            if book["description"]:
                                st.write(
                                    book["description"][:350] + (
                                        "..." if len(book["description"]) > 350 else ""
                                    )
                                )

                            if book["preview"]:
                                st.markdown(
                                    f"[Preview book]({book['preview']})"
                                )

                            if book["info_link"]:
                                st.markdown(
                                    f"[More book details]({book['info_link']})"
                                )

                            if not book["preview"]:
                                st.caption(
                                    "Preview link is not available for this result."
                                )
                else:
                    st.info("No online results found. Try another search.")

    # ---------------- ADD BOOK ----------------
    with add_tab:
        st.subheader("Add a Book to Your Library")

        with st.form("add_book_form"):
            title = st.text_input("Book Title")
            book_class = st.text_input("Class")
            book_board = st.text_input("Board")
            subject = st.text_input("Subject")
            medium = st.selectbox(
                "Medium",
                ["English", "Hindi", "Other"]
            )
            pdf_url = st.text_input("Verified textbook or PDF link")

            submitted = st.form_submit_button("Save Book")

            if submitted:
                if title.strip():
                    add_book(
                        title.strip(),
                        book_class,
                        book_board,
                        subject,
                        medium,
                        pdf_url.strip()
                    )
                    st.success("Book saved to your library!")
                else:
                    st.warning("Please enter a book title.")

    # ---------------- KNOWLEDGE AI ----------------
    with ai_tab:
        st.subheader("Ask Knowledge AI")

        question = st.text_area(
            "Ask an educational question",
            placeholder="Example: Explain photosynthesis in simple words."
        )

        if st.button("Ask Knowledge AI", type="primary"):
            if question.strip():
                prompt = f"""
You are SmartGaon AI Knowledge Assistant.
Explain educational topics in simple, student-friendly language.
Use headings and examples where useful.
If you are unsure about a fact, clearly say so.

Student question:
{question}
"""
                with st.spinner("Preparing your answer..."):
                    answer, error = ask_groq(prompt)

                if error:
                    st.error(error)
                else:
                    st.markdown("### Answer")
                    st.write(answer)
            else:
                st.warning("Please enter a question.")

    # ---------------- SOLVE QUESTION ----------------
    with solve_tab:
        st.subheader("Question Helper")

        question_text = st.text_area(
            "Enter your textbook question",
            placeholder="Type your question here..."
        )

        if st.button("Explain My Question", type="primary"):
            if question_text.strip():
                prompt = f"""
Explain this school question step by step.
Use simple language.
Do not invent missing information.

Question:
{question_text}
"""
                with st.spinner("Solving your question..."):
                    answer, error = ask_groq(prompt)

                if error:
                    st.error(error)
                else:
                    st.markdown("### Explanation")
                    st.write(answer)
            else:
                st.warning("Please enter a question.")
