from ..table_stream_tgt import TableStreamTgt
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, LongType


class Inr_provider(TableStreamTgt):

    header_key = "provider_references"

    provider_groups = ArrayType(StructType([
                                  StructField("npi", ArrayType(StringType()), False),
                                  StructField("tin", StructType([
                                    StructField("type", StringType(), False),
                                    StructField("value", StringType(), False)]), False)]))

    definition = \
        [("file_name",         StringType(),    False, "File name of in network rate json"),
         ("batch_id",          LongType(),      True,  "Streaming ingest batchId"),
         ("provider_group_id", LongType(),      False, "Publisher defined id reference code"),
         ("provider_groups",   provider_groups, True,  "Group of providers as organized by publisher"),
         ("location",          StringType(),    True,  "URL of download if not provided in provider_groups")]
