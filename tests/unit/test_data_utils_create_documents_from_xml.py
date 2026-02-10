import pytest
import tempfile
from pathlib import Path

from data_utils import create_documents_from_xml


@pytest.fixture
def temp_dir_with_valid_tmx():
    """Create a temporary directory with a valid TMX file."""
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1" datatype="PlainText" segtype="sentence" adminlang="EN-US" srclang="be" o-tmf="LogiTermBT"/>
        <body>
            <tu>
                <tuv xml:lang="de" creationid="ALIGN!">
                    <seg>Hello World</seg>
                </tuv>
                <tuv xml:lang="en" creationid="ALIGN!">
                    <seg>Hallo Welt</seg>
                </tuv>
            </tu>
            <tu>
                <tuv xml:lang="de" creationid="ALIGN!">
                    <seg>Good morning</seg>
                </tuv>
                <tuv xml:lang="en" creationid="ALIGN!">
                    <seg>Guten Morgen</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "test.tmx"
        file_path.write_text(xml_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_multiple_files():
    """Create a temporary directory with multiple TMX files."""
    file1_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>File 1 Text 1</seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>File 1 Text 1 EN</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    file2_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="fr">
                    <seg>File 2 Text 1</seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>File 2 Text 1 EN</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "file1.tmx").write_text(file1_content, encoding="utf-8")
        Path(tmpdir, "file2.tmx").write_text(file2_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_nested_files():
    """Create a temporary directory with nested TMX files."""
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>Nested file text</seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>Nested file text EN</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        subdir = Path(tmpdir) / "subdir"
        subdir.mkdir()
        (subdir / "nested.tmx").write_text(xml_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_invalid_xml():
    """Create a temporary directory with an invalid XML file."""
    invalid_content = """<tmx version="1.4">
        <header/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>Invalid XML
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "invalid.tmx").write_text(invalid_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_single_tuv():
    """Create a temporary directory with a file containing only one TUV (should be skipped)."""
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>Only one language</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "single.tmx").write_text(xml_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_empty_seg():
    """Create a temporary directory with empty seg elements."""
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg></seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>Valid text</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "empty.tmx").write_text(xml_content, encoding="utf-8")
        yield tmpdir


@pytest.fixture
def temp_dir_with_hidden_files():
    """Create a temporary directory with hidden files that should be ignored."""
    xml_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>Visible file</seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>Visible file EN</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    hidden_content = """<tmx version="1.4">
        <header creationtool="AlignEditor" creationtoolversion="1.1"/>
        <body>
            <tu>
                <tuv xml:lang="de">
                    <seg>Hidden file</seg>
                </tuv>
                <tuv xml:lang="en">
                    <seg>Hidden file EN</seg>
                </tuv>
            </tu>
        </body>
    </tmx>"""

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "visible.tmx").write_text(xml_content, encoding="utf-8")
        Path(tmpdir, ".hidden.tmx").write_text(hidden_content, encoding="utf-8")
        yield tmpdir


class TestCreateDocumentsFromXml:
    """Test suite for create_documents_from_xml function."""

    def test_creates_documents_from_valid_tmx(self, temp_dir_with_valid_tmx):
        """Test that documents are created correctly from valid TMX file."""
        documents, files = create_documents_from_xml(temp_dir_with_valid_tmx)

        # Should have 2 documents from 2 translation units
        assert len(documents) == 2
        assert len(files) == 1

        # Check first document
        assert documents[0]["lang"] == "de"
        assert documents[0]["text"] == "Hello World"
        assert documents[0]["tr_lang"] == "en"
        assert documents[0]["tr_text"] == "Hallo Welt"
        assert documents[0]["file_id"] == 0

        # Check second document
        assert documents[1]["lang"] == "de"
        assert documents[1]["text"] == "Good morning"
        assert documents[1]["tr_lang"] == "en"
        assert documents[1]["tr_text"] == "Guten Morgen"
        assert documents[1]["file_id"] == 0

        # Check files metadata
        assert files[0]["id"] == 0
        assert files[0]["docs_num"] == 2

    def test_handles_multiple_files(self, temp_dir_with_multiple_files):
        """Test that multiple TMX files are processed correctly."""
        documents, files = create_documents_from_xml(temp_dir_with_multiple_files)

        # Should have 2 files with 1 document each
        assert len(files) == 2
        assert len(documents) == 2

        # Check file IDs are incremented correctly
        assert files[0]["id"] == 0
        assert files[1]["id"] == 1

        # Check file_id in documents matches
        assert documents[0]["file_id"] == 0
        assert documents[1]["file_id"] == 1

    def test_handles_nested_directories(self, temp_dir_with_nested_files):
        """Test that files in nested directories are found and processed."""
        documents, files = create_documents_from_xml(temp_dir_with_nested_files)

        assert len(files) == 1
        assert len(documents) == 1

        # Check that the nested file path is stored
        assert "subdir" in files[0]["path"]
        assert documents[0]["text"] == "Nested file text"

    def test_handles_invalid_xml_gracefully(self, temp_dir_with_invalid_xml, capsys):
        """Test that invalid XML files are skipped with appropriate warnings."""
        documents, files = create_documents_from_xml(temp_dir_with_invalid_xml)

        # Invalid XML should be skipped
        assert len(files) == 0
        assert len(documents) == 0

        # Check that error was printed
        captured = capsys.readouterr()
        assert "Failed to process" in captured.out

    def test_skips_single_tuv_entries(self, temp_dir_with_single_tuv, capsys):
        """Test that translation units with only one language are skipped."""
        documents, files = create_documents_from_xml(temp_dir_with_single_tuv)

        # Single TUV should not create a document
        assert len(documents) == 0

        # But file should still be recorded
        assert len(files) == 1
        assert files[0]["docs_num"] == 0

        # Check warning was printed
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "1 tuvs" in captured.out

    def test_skips_incomplete_content(self, temp_dir_with_empty_seg, capsys):
        """Test that entries with missing text are skipped."""
        documents, files = create_documents_from_xml(temp_dir_with_empty_seg)

        # Empty seg should result in incomplete content
        assert len(documents) == 0
        assert len(files) == 1
        assert files[0]["docs_num"] == 0

    def test_ignores_hidden_files(self, temp_dir_with_hidden_files):
        """Test that hidden files (starting with .) are ignored."""
        documents, files = create_documents_from_xml(temp_dir_with_hidden_files)

        # Only visible file should be processed
        assert len(files) == 1
        assert len(documents) == 1
        assert "visible.tmx" in files[0]["path"]

    def test_file_metadata_is_correct(self, temp_dir_with_valid_tmx):
        """Test that file metadata contains correct information."""
        documents, files = create_documents_from_xml(temp_dir_with_valid_tmx)

        assert len(files) == 1
        file_info = files[0]

        assert "id" in file_info
        assert "path" in file_info
        assert "docs_num" in file_info
        assert file_info["docs_num"] == 2
        assert isinstance(file_info["path"], str)

    def test_document_structure_is_correct(self, temp_dir_with_valid_tmx):
        """Test that each document has the correct structure."""
        documents, files = create_documents_from_xml(temp_dir_with_valid_tmx)

        required_keys = {"lang", "text", "tr_lang", "tr_text", "file_id"}

        for doc in documents:
            assert set(doc.keys()) == required_keys
            assert doc["lang"] is not None
            assert doc["text"] is not None
            assert doc["tr_lang"] is not None
            assert doc["tr_text"] is not None
            assert isinstance(doc["file_id"], int)

    def test_empty_directory(self):
        """Test handling of empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            documents, files = create_documents_from_xml(tmpdir)

            assert len(documents) == 0
            assert len(files) == 0
