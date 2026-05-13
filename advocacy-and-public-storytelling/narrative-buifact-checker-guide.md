# Fact-Checker Tool

The Fact-Checker reviews generated narratives against the source material provided.

It helps identify:

- unsupported claims
- invented details
- overstatement
- vague claims
- risky generalisations
- cultural flattening
- statements requiring community review

## What it checks

The tool asks:

- Is this claim supported by the source material?
- Did the AI invent names, dates, places, rituals, or historical claims?
- Did the narrative overstate certainty?
- Did it flatten Orang Laut, Orang Pulau, or island communities?
- Does any statement require community review?

## Important limitation

This tool does not verify against external sources.

It only checks whether the generated narrative is supported by the source material provided.

## Output

The tool creates:

`fact-check-report.json`

## Recommended workflow

1. Generate a narrative
2. Run the fact-checker
3. Review flagged issues
4. Revise the narrative
5. Seek community or human review where needed
6. Publish only reviewed material
