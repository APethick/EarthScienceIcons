# Permanent published icon identities

- Every published icon ID, Unicode designation and fallback character is permanent. This is a strict compatibility requirement for all future work.
- Treat `icon-identities.json` as an append-only ledger. Never modify or delete an existing record, renumber icons, reuse allocated codepoints, or regenerate the ledger from source files or generated output.
- Artwork, descriptions and display names may change while retaining the original ID, Unicode and fallback. Retain deprecated glyphs and mappings.
- Append new icons to the catalogue. Append ledger records with unused private-use codepoints strictly above the current maximum and unused fallback characters. Preserve existing catalogue order and fallback assignments.
- Keep identity validation enabled in font, flat SVG, site and distribution builds. Fix the source when validation fails; never bypass validation or update historical fixtures to accept renumbering.
- Before delivery, run the identity regression tests and distribution verification. Report any compatibility failure rather than shipping it.
