import argparse
from scholix.converter import createScholixV4
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os
import shutil

class DumpToScholixConverter:
    def __init__(self,relationships_path:str, entities_path:str, target_path:str, datasourceFilter=None, relationFilter=None, sourcePidFilter=None, targetPidFilter=None):
        self.relationships_path = relationships_path
        self.entities_path = entities_path
        self.target_path = target_path
        self.datasourceFilter = datasourceFilter
        self.relationFilter = relationFilter
        self.sourcePidFilter = sourcePidFilter
        self.targetPidFilter = targetPidFilter
        
        self.spark = SparkSession.builder.appName("Scholexplorer-Dump-Processing").getOrCreate()

    def convert(self):
        relDS = self.spark.read.json(self.relationships_path)
        entitiesDS = self.spark.read.json(self.entities_path)
        s_entities = entitiesDS.select([F.col(c).alias(f"s_{c}") for c in entitiesDS.columns])
        t_entities = entitiesDS.select([F.col(c).alias(f"t_{c}") for c in entitiesDS.columns])
        if (self.datasourceFilter is not None and len(self.datasourceFilter) > 0):
            relDS = relDS.filter(F.expr(f"array_contains(transform(linkProviders, x -> lower(x)), '{self.datasourceFilter.lower()}')"))
        if (self.relationFilter is not None and len(self.relationFilter) > 0):
            relDS = relDS.filter(F.expr(f"lower(relationType) = '{self.relationFilter.lower()}'"))
        if (self.sourcePidFilter is not None and len(self.sourcePidFilter) > 0):
            relDS = relDS.filter(F.expr(f"array_contains(transform(sourcePidType, x -> lower(x)), '{self.sourcePidFilter.lower()}')"))
        if (self.targetPidFilter is not None and len(self.targetPidFilter) > 0):
            relDS = relDS.filter(F.expr(f"array_contains(transform(targetPidType, x -> lower(x)), '{self.targetPidFilter.lower()}')"))
        scholix_df =relDS.join(s_entities, relDS.sourceId == s_entities.s_dnetIdentifier)\
            .join(t_entities, relDS.targetId == t_entities.t_dnetIdentifier)\
            .rdd.map(createScholixV4)
        scholix_df.saveAsTextFile(self.target_path, compressionCodecClass="org.apache.hadoop.io.compress.GzipCodec")
        
        

    def _filter_record(self, record):
        # Implement the filtering logic here
        if (self.datasourceFilter and record['datasource'] != self.datasourceFilter):
            return False
        if (self.relationFilter and record['relation'] != self.relationFilter):
            return False
        if (self.sourcePidFilter and record['sourcePid'] != self.sourcePidFilter):
            return False
        if (self.targetPidFilter and record['targetPid'] != self.targetPidFilter):
            return False
        return True

    def _convert_record_to_scholix(self, record):
        # Implement the conversion logic here
        scholix_record = {
            'source': record['source'],
            'target': record['target'],
            'relation': record['relation'],
            'datasource': record['datasource']
        }
        return scholix_record
    
    
    

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert dump to Scholix format.')
    parser.add_argument('dump_path', type=str, help='Path to the dump file containing the relationships and entities folder')
    parser.add_argument('scholix_path', type=str, help='Path to the scholix generated dump')
    parser.add_argument('--datasourceFilter', type=str, default=None, help='Filter by datasource')
    parser.add_argument('--relationFilter', type=str, default=None, help='Filter by relation')
    parser.add_argument('--sourcePidFilter', type=str, default=None, help='Filter by source PID')
    parser.add_argument('--targetPidFilter', type=str, default=None, help='Filter by target PID')
    return parser.parse_args()

def main():
    args = parse_arguments()

    if os.path.exists(args.scholix_path):
        shutil.rmtree(args.scholix_path)

    converter = DumpToScholixConverter(
        relationships_path=f"{args.dump_path}/relationships",
        entities_path=f"{args.dump_path}/entities",
        target_path=args.scholix_path,
        datasourceFilter=args.datasourceFilter,
        relationFilter=args.relationFilter,
        sourcePidFilter=args.sourcePidFilter,
        targetPidFilter=args.targetPidFilter
    )
    
    scholix_data = converter.convert()
    
    # print(json.dumps(scholix_data, indent=2))

if __name__ == '__main__':
    main()