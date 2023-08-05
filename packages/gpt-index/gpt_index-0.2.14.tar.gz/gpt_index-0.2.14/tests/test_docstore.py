"""Test docstore."""

from gpt_index.data_structs.data_structs import Node
from gpt_index.docstore import DocumentStore
from gpt_index.readers.schema.base import Document


def test_docstore() -> None:
    """Test docstore."""
    doc = Document("hello world", doc_id="d1", extra_info={"foo": "bar"})
    node = Node("my node", doc_id="d2", node_info={"node": "info"})

    # test get document
    docstore = DocumentStore.from_documents([doc, node])
    gd1 = docstore.get_document("d1")
    assert gd1 == doc
    gd2 = docstore.get_document("d2")
    assert gd2 == node

    # test serialize/deserialize
    doc_dict = docstore.serialize_to_dict()
    assert doc_dict["docs"] == {
        "d1": {
            "text": "hello world",
            "doc_id": "d1",
            "embedding": None,
            "extra_info": {"foo": "bar"},
            "__type__": "Document",
        },
        "d2": {
            "text": "my node",
            "doc_id": "d2",
            "embedding": None,
            "extra_info": None,
            "node_info": {"node": "info"},
            "index": 0,
            "child_indices": [],
            "ref_doc_id": None,
            "__type__": "node",
        },
    }

    docstore_loaded = DocumentStore.load_from_dict(doc_dict)
    assert docstore_loaded == docstore
