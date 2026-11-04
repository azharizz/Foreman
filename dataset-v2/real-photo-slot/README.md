# Slot for real photos (empty on purpose)

The photos in `nas-upload/` are **synthetic illustrations** labelled "NOT A REAL PHOTO". They cannot test UGREEN's real photo search or vision models. This slot is where the team can add up to three real photos later.

**Rules for real photos**
- Take them yourself. Show only a door, a wall or a ceiling. No people, faces, number plates, screens or anything that identifies a place.
- Remove GPS before adding them (for example `exiftool -gps:all= file.jpg`), or replace it with the Alpha site reference point from the contract (`-6.90000, 107.60000`, an arbitrary synthetic coordinate).
- Set the capture date (EXIF DateTimeOriginal) to the record you want the photo to support.

| Slot | Copy to | Set EXIF date to | Should corroborate |
|---|---|---|---|
| REAL_01 | `nas-upload/Project-Alpha/06-Site-Photos/REAL_01.jpg` | 2026-10-15 | Doors installed (SR-2026-10-15, INV-010) |
| REAL_02 | `nas-upload/Project-Alpha/06-Site-Photos/REAL_02.jpg` | 2026-08-26 | Fire-rated partitions (INV-006) |
| REAL_03 | `nas-upload/Project-Alpha/06-Site-Photos/REAL_03.jpg` | 2026-09-28 | Duct re-routing (CO-005) |

The three rows are already in `MANIFEST.csv` with kind `real-photo-slot` and status `EMPTY`. When you add a photo, fill in its date, SHA-256 and size in the manifest and add a line to `VERIFICATION.md`. Real photos only add corroboration. They do not change any expected class in the answer key.
