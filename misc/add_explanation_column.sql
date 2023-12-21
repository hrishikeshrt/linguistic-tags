/* Add "explanation" field to all data tables except VerbalRoot table (which already had it) */
/* Run these commands in the SQLite3 console */
/* CAUTION: You need to use this only if updating from commit id 3c84b46622a223994604846dbd18f357f6995240 */

ALTER TABLE "sentence_meaning_data" ADD COLUMN explanation TEXT;
ALTER TABLE "sentence_structure_data" ADD COLUMN explanation TEXT;
ALTER TABLE "voice_data" ADD COLUMN explanation TEXT;
ALTER TABLE "dependency_data" ADD COLUMN explanation TEXT;
ALTER TABLE "parts_of_speech_data" ADD COLUMN explanation TEXT;
ALTER TABLE "morphology_data" ADD COLUMN explanation TEXT;
ALTER TABLE "verbal_data" ADD COLUMN explanation TEXT;
ALTER TABLE "tense_aspect_mood_data" ADD COLUMN explanation TEXT;
ALTER TABLE "group_data" ADD COLUMN explanation TEXT;