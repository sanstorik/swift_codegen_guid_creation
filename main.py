import xml.etree.ElementTree as ET
import inflect as Plural

output = file("output.txt", "a+")

def create_guid_extension(entity_xml):
    entity_name = entity_xml.get("name")
    plural_entity_name = Plural.engine().plural(entity_name)

    output.write("\n\nextension {}: GUIDMapEntity {} \n".format(entity_name, "{"))
    output.write("    var syncEntity: SyncEntityType { return SyncEntity.%s }" % (plural_entity_name))
    output.write("\n\n    func process(in context: NSManagedObjectContext, _ fetcher: GuidFetcher) {")
    output.write("\n\tappendSelf(in: context, fetcher)")

    write_inner_relationships(entity_xml)

    output.write("\n    }")
    output.write("\n}")


def write_inner_relationships(entity_xml):
    inner_relationships = entity_xml.findall("relationship")
    single_inner_relationships = filter(lambda x: x.get("toMany") == "NO" or x.get("toMany") is None, inner_relationships)
    tomany_inner_relationships = filter(lambda x: x.get("toMany") == "YES", inner_relationships)

    for inner_relationship in single_inner_relationships:
        inner_entity_name = inner_relationship.get("name")
        output.write("\n\t{}?.appendSelf(in: context, fetcher)".format(inner_entity_name))

    if len(tomany_inner_relationships) > 0:
        output.write("\n")

    for inner_relationship in tomany_inner_relationships:
        inner_entity_name = inner_relationship.get("name")
        output.write("\n\tfor entity in %s {" % (inner_entity_name))
        output.write("\n\t    entity.appendSelf(in: context, fetcher)")
        output.write("\n\t}")



if __name__ == "__main__":
    file("output.txt", "w+").close()
    core_data_xml = ET.parse("contents").getroot()

    for entity_xml in core_data_xml.findall("entity"):
        if len(filter(lambda x: x.get("name") == "created", entity_xml.findall("attribute"))) > 0:
            create_guid_extension(entity_xml)