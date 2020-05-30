from elasticsearch_dsl import Document, Text


class eBPFProgramInstanceDocument(Document):
    ebpf_program_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)

    class Index:
        name = 'ebpf-program-instance'
