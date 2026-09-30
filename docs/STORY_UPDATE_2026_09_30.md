# September 30 screenplay update

Chapter one now continues through chapter_two after its day summary. The first-day gazebo approach, escape, escort and Badral choices follow the revised source.

The continuation includes 20 choice groups: classroom rumours and sandwich rejection, the sister call, Saruul’s job loss and family disclosure, dinner with her siblings, Khulan’s late arrival, the father/sister confrontation, a second desktop chat, and Chingun’s crisis the following morning. The final test-results line is presented as the sister’s message. Choices and discovered secrets use save-backed story_flags. Saruul’s promise choice updates her relationship score.

The sister call allows two declines before accepting. The existing desktop opens without resetting Bolor’s relationship or block state. Saruul’s living room has three inspectable items. Existing character test images remain in use. Final video/audio are not supplied by this document; saruul_home.webp and school_restroom.webp can replace the neutral background fallback under game/images/story/.

Chat boundaries now issue an explicit first warning and a final warning at three strikes. Repeated harmful messages at two/three strikes trigger another 120-second pause. Apologies do not erase strikes or award relationship points. Four strikes reject backend requests even if the blocked flag is absent. Delayed client responses cannot clear a block or shorten an active pause. Live AI behavior requires deploying the updated backend.

Validation: 16 backend tests; Ren’Py 8.4.1 lint; four automated continuation traversals choosing A/B/C/D respectively, asserting all 20 choice flags and completion. Device and inspection screens were substituted with automatic returns only in the temporary test harness, which is not shipped. No live model or Render deployment was tested.
