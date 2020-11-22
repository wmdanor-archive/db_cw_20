CREATE OR REPLACE FUNCTION trgfunc_artist() RETURNS TRIGGER as $$
BEGIN
	IF NEW.name != OLD.name OR NEW.comment != OLD.comment THEN
		IF NEW.comment IS NOT NULL THEN
			UPDATE artists
			SET artists.search_tsv = make_tsvector(NEW.name, NEW.comment)
			WHERE artists.artist_id = NEW.artist_id;
		ELSE
			UPDATE artists
			SET artists.search_tsv = make_tsvector(NEW.name, '')
			WHERE artists.artist_id = NEW.artist_id;
		END IF;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER artist_update_tsv_trg
    AFTER INSERT OR UPDATE ON artists
	FOR EACH ROW EXECUTE PROCEDURE trgfunc_artist();
	

CREATE OR REPLACE FUNCTION trgfunc_composition() RETURNS TRIGGER as $$
BEGIN
	IF NEW.title != OLD.title OR NEW.lyrics != OLD.lyrics THEN
		IF NEW.lyrics IS NOT NULL THEN
			UPDATE compositions
			SET compositions.search_tsv = make_tsvector(NEW.title, NEW.lyrics)
			WHERE compositions.composition_id = NEW.composition_id;
		ELSE
			UPDATE compositions
			SET compositions.search_tsv = make_tsvector(NEW.title, '')
			WHERE compositions.composition_id = NEW.composition_id;
		END IF;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER composition_update_tsv_trg
    AFTER INSERT OR UPDATE ON compositions
	FOR EACH ROW EXECUTE PROCEDURE trgfunc_composition();