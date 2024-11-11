from scholix.model import *
def createScholixV4(r) -> Scholix:
    """
    Converts a Spark Row containing a join between relationships and entities into a Scholix dictionary.
    Args:
        r (Row): A Spark Row object containing the following fields:
            - s_identifier: List of source identifiers.
            - s_objectType: Source object type.
            - s_objectSubType: Source object subtype.
            - s_title: Source title.
            - s_creator: List of source creators.
            - s_publicationDate: Source publication date.
            - s_publisher: List of source publishers.
            - t_identifier: List of target identifiers.
            - t_objectType: Target object type.
            - t_objectSubType: Target object subtype.
            - t_title: Target title.
            - t_creator: List of target creators.
            - t_publicationDate: Target publication date.
            - t_publisher: List of target publishers.
            - publicationDate: Link publication date.
            - linkProviders: List of link providers.
            - relationType: Type of relationship.
    Returns:
        dict: A dictionary representation of the Scholix object.
    """

relationMap = {"issupplementto": "IsSupplementTo", 
               "issupplementedby":"IsSupplementedBy", 
               "references":"References", 
               "isreferencedby":"IsReferencedBy", 
               "isrelatedto":"IsRelatedTo"}


def createScholixV4(r)-> Scholix:
    
    sourceE = ScholixResource(
        Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=i.url) for i in r.s_identifier] if r.s_identifier else [],
        Type=r.s_objectType,
        SubType=r.s_objectSubType,
        Title=r.s_title,
        Creator=[ Creator(Name=c.name, 
                    Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=None) for i in c.identifiers] if c.identifiers else [])
                    for c in r.s_creator] if r.s_creator else [],
        PublicationDate=r.s_publicationDate,
        Publisher=[Publisher(name=p.name, Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=i.url) for i in p.identifiers]) for p in r.s_publisher])

    targetE = ScholixResource(
        Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=i.url) for i in r.s_identifier] if r.t_identifier else [],
        Type=r.t_objectType,
        SubType=r.t_objectSubType,
        Title=r.t_title,
        Creator=[ Creator(Name=c.name, 
                    Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=None) for i in c.identifiers] if c.identifiers else [])
                    for c in r.t_creator] if r.t_creator else [],
        PublicationDate=r.t_publicationDate,
        Publisher=[Publisher(name=p.name, Identifier=[Identifier(ID=i.identifier, IDScheme=i.schema, IDURL=i.url) for i in p.identifiers]) for p in r.t_publisher]
    )

    s = Scholix(
        LinkPublicationDate=  r.publicationDate,
        LinkProvider= [LinkProvider(name=k, identifier=[]) for k in r.linkProviders],
        RelationshipType= RelationshipType(Name=relationMap.get(r.relationType, "IsRelatedTo"), SubType=r.relationType, SubTypeSchema="https://schema.datacite.org/meta/kernel-4.0/metadata.xsd"),
        LicenseURL=None,
        Source=sourceE,
        Target=targetE)
    return s.to_dict()