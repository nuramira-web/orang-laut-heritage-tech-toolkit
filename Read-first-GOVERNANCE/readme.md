
Governance, Consent, and Cultural Authority

This folder holds the cultural-data-governance layer of the Orang Laut Heritage Tech Toolkit. It defines how materials enter the archive, under what consent, with what attached protocols, and how cultural authority is honoured at every stage of the digital lifecycle.

The governance layer sits underneath the code. No item should be ingested, displayed, processed by AI tools, or surfaced through Ask Pulau Brani without first passing through these documents.

What is here
LOCAL_CONTEXTS_LABELS_REFERENCE.md: Full reference for the four Local Contexts  - Notices and twenty TK Labels, with guidance on when each applies.

CONSENT_AGREEMENT_TEMPLATE.md: Plain-language consent form for contributors and tradition-bearers. Bilingual (English / Bahasa Melayu) skeleton.

METADATA_SCHEMA.md: The cataloging schema used across all toolkit modules, including Local Contexts fields.

catalog_entry_template.md: A blank, fillable template for a single archive item.

catalog_entry_example.mdA worked example showing the template populated.

The framework, in one paragraph
The toolkit grounds its data governance in two interlocking standards. The CARE Principles for Indigenous Data Governance (Collective Benefit, Authority to Control, Responsibility, Ethics) set the values. The Local Contexts framework operationalises those values through machine-readable Notices and Labels that travel with the data wherever it goes. Together with FAIR (Findable, Accessible, Interoperable, Reusable), these form a stack: FAIR makes data useful, CARE makes data ethical, and Local Contexts makes both visible in the metadata itself.

Important framing note
Local Contexts and TK Labels were developed primarily by and for Indigenous communities in settler-colonial contexts. The framework is increasingly being adopted by other communities whose cultural heritage has been displaced, fragmented, or held by external institutions — which includes the Orang Laut, Orang Pulau, and southern islanders of Singapore.

Whether and how this community wishes to position itself in relation to the global Indigenous data sovereignty movement is a decision for the community itself, not for the toolkit's authors. The toolkit provides the infrastructure; the community provides the authority. This folder is written to support that decision-making, not pre-empt it.

Sequencing: how to actually roll this out

Register the project on the Local Contexts Hub (localcontextshub.org) as an Institution or Researcher account. This generates the project URIs that get embedded in your metadata.

Apply the four Notices (TK, BC, Attribution Incomplete, Open to Collaborate) as project-level placeholders. These signal that this is a heritage project with cultural rights and responsibilities attached, and that Labels are under development.
Begin community engagement through the Youth Co-Creation Lab, elder workshops, and Pulau Brani Project partners. The goal is co-creating a customised suite of TK Labels — title text, default text, translations into local Malay — that the community will then own and apply.

Establish a community decision-making body (council, advisory circle, named tradition-bearers) empowered to approve Label customisation and item-level Label application. Document its composition and process.

Apply Labels at the item level once the community has authorised them. Until then, items carry the project-level Notices.
Make Labels and Notices visible at every point the material is displayed: in the Community Archive, on Memory Map markers, in Ask Pulau Brani responses, in Memory Constellation Engine results, and in any export or API response.


Hard rules

Icons are not modifiable. Local Contexts icons are internationally recognisable and protected. Use them exactly as provided.
Notices do not require community sign-off, but Labels do. Do not invent or apply a Label without community authority.
Consent is revocable. A contributor can withdraw an item at any time. The system must support this; see CONSENT_AGREEMENT_TEMPLATE.md.

Sacred and gender-restricted material does not transit through general-purpose AI systems. Items carrying TK Secret/Sacred, TK Women Restricted, or TK Men Restricted Labels are excluded from Ask Pulau Brani training and retrieval, and from the Memory Constellation Engine's public surface.

Every export carries the Notices and Labels. Metadata travels with the data.


Related standards

CARE Principles — gida-global.org/care
FAIR Principles — go-fair.org/fair-principles
Local Contexts — localcontexts.org
Mukurtu CMS — mukurtu.org (prior art: a community-controlled archive platform with TK Labels built in)
