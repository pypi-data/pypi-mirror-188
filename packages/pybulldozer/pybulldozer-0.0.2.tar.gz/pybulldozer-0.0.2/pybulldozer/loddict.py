""" Dictionary that holds multiple tables in the following : [list of records of that table]
Used for flattening non-relation data """
from pybulldozer.helpers import logger


class Lod_dict:
    """ example:
        {
            products: [array of products]
            subproducts: [array of products
        }
    """
    __lod_dict: {str: list} = {}

    def debug(self, sample:bool=True):
        for name, records in self.__lod_dict.items():
            hasrecords = len(records) > 0
            print(f"{name} ({len(records)} records) {'example:' if (hasrecords and sample) else ''}")
            if (hasrecords):
                if (sample):
                    print(f"\t{records[0]}")
                    # for k,v in records[0].items():
                    #     print(f"\t{k} \t\t\t {v}")
                else:
                    for record in records:
                        print(f"\t{record}")

    def add(self, name: str, record: dict):
        if (name in list(self.__lod_dict)):
            self.__lod_dict[name].append(record)
        else:
            self.__lod_dict[name] = [record]


