insert into gridMng_state (name) values ('finish');
insert into gridMng_state (name) values ('initial');
insert into gridMng_state (name) values ('check');
insert into gridMng_state (name) values ('waitingForAltAndCon');
insert into gridMng_state (name) values ('waitingForWeightsAndRatings');

--DELIMITER $$
--CREATE TRIGGER check_if_participant BEFORE INSERT ON sharedGrid_responsegrid FOR EACH ROW   
--BEGIN   
--    IF (select count('user') from sharedGrid_userparticipatesession where session= (select session from sharedGrid_sessiongrid where iternation = NEW.iteration AND grid = NEW.grid) AND user = NEW.'user') <= 0 THEN
--   	 RAISERROR 50009 'User is not participating in the session';
--    END IF;
--END; $$