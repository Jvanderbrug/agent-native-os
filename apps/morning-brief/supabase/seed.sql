-- Optional. Loads two demo briefs so the homepage isn't empty on first deploy.
-- Run after 0001_morning_brief.sql. Safe to re-run (uses on-conflict-do-nothing).

insert into public.briefs (date, title, summary, top_priority, sections, source_status, delivery_status)
values
(
  current_date,
  'Demo brief: ship the capstone today',
  'Two sources synced, three calendar events flagged, one priority. Telegram ping queued. Replace this with a real brief once your sources are wired.',
  'Pair with one student during the 2pm checkpoint to unblock their Vercel deploy.',
  '[
    {"heading": "Schedule", "body": "10am workshop kickoff. 2pm deploy checkpoint. 5pm demo wall."},
    {"heading": "Open loops", "body": "Two students still need Telegram chat ids. Walk them through @BotFather then getUpdates."},
    {"heading": "Risk", "body": "Vercel env vars in the wrong project. Double-check before students paste secrets."}
  ]'::jsonb,
  '[
    {"name": "manual-notes", "enabled": true, "last_pulled_at": null, "item_count": 3},
    {"name": "calendar", "enabled": true, "last_pulled_at": null, "item_count": 5},
    {"name": "gmail", "enabled": false, "last_pulled_at": null, "item_count": 0}
  ]'::jsonb,
  '{"channel": "telegram", "delivered_at": null, "recipient": "your-chat-id", "ok": false}'::jsonb
)
on conflict do nothing;

insert into public.briefs (date, title, summary, top_priority, sections, source_status, delivery_status)
values
(
  current_date - interval '1 day',
  'Yesterday: dress rehearsal',
  'Five test runs, two failures, three clean. Telegram ping latency under 800ms.',
  'Lock the env vars before tomorrow.',
  '[
    {"heading": "Wins", "body": "Brief contract validated end to end."},
    {"heading": "Cuts", "body": "Skipped Slack adapter for Sunday. Telegram only."}
  ]'::jsonb,
  '[
    {"name": "manual-notes", "enabled": true, "last_pulled_at": null, "item_count": 1}
  ]'::jsonb,
  '{"channel": "telegram", "delivered_at": null, "recipient": "your-chat-id", "ok": true}'::jsonb
)
on conflict do nothing;
