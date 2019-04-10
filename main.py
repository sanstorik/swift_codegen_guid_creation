import xml.etree.ElementTree as ET

output = file("output.txt", "a+")

def create_guid_extension(entity_xml):
    entity_name = entity_xml.get("name")
    output.write("\nextension {} {} \n".format(entity_name, "{"))
    output.write("    var syncEntity: SyncEntityType { return SyncEntity.%s }" % (entity_name + "s"))
    output.write("\n\n    func process(in context: NSManagedObjectContext, _ fetcher: GuidFetcher) {")
    output.write("\n\tappendSelf(in: context, fetcher)")

    for inner_relationship in entity_xml.findall("relationship"):
        inner_entity_name = inner_relationship.get("name")
        output.write("\n\t{}?.appendSelf(in: context, fetcher)".format(inner_entity_name))

    output.write("\n    }")
    output.write("\n}")


if __name__ == "__main__":
    file("output.txt", "w+").close()
    core_data_xml = ET.parse("contents").getroot()

    for entity_xml in core_data_xml.findall("entity"):
        create_guid_extension(entity_xml)