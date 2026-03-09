import os
import pytest
from tf.fabric import Fabric

@pytest.fixture(scope="module")
def tf_api():
    tf_dir = os.path.expanduser('~/tmp/web-c/tf')
    TF = Fabric(locations=tf_dir)
    api = TF.load('')
    return api

def test_node_mapping(tf_api):
    # Verify we can find a standard verse using nodeFromSection
    node = tf_api.T.nodeFromSection(('GEN', 1, 3))
    assert node is not None, "Failed to resolve GEN 1:3 node"

def test_punctuation_and_smart_quotes_gen_1_3(tf_api):
    node = tf_api.T.nodeFromSection(('GEN', 1, 3))
    text = tf_api.T.text(node)
    assert "Let there be light" in text
    assert "“" in text, "Missing opening smart quote"
    assert "”" in text, "Missing closing smart quote"

def test_punctuation_and_smart_quotes_gen_2_23(tf_api):
    node = tf_api.T.nodeFromSection(('GEN', 2, 23))
    text = tf_api.T.text(node)
    assert "woman" in text
    assert "‘" in text, "Missing single opening smart quote"
    assert "’" in text, "Missing single closing smart quote"

def test_mid_word_apostrophe(tf_api):
    # Check Gen 1:2 for "God’s"
    node = tf_api.T.nodeFromSection(('GEN', 1, 2))
    text = tf_api.T.text(node)
    # Ensure it's not split into "God s"
    assert "God’s" in text, f"Apostrophe incorrectly split in: {text}"

def test_matthew_corruption_fix(tf_api):
    node = tf_api.T.nodeFromSection(('Matthew', 5, 3))
    text = tf_api.T.text(node)
    assert "Blessed are the poor in spirit" in text
    assert "strong" not in text

def test_book_count(tf_api):
    books = list(tf_api.F.otype.s('book'))
    assert len(books) == 73, f"Expected 73 books, found {len(books)}"
    assert tf_api.F.book.v(books[0]) == 'GEN'
    assert tf_api.F.book.v(books[-1]) == 'Revelation'
