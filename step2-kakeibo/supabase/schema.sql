-- ごま家計簿: Supabase の SQL Editor に貼り付けて「Run」する

create table if not exists public.entries (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  date       date not null,
  amount     integer not null check (amount > 0 and amount < 100000000),
  cat        text not null check (cat in ('food', 'daily', 'move', 'fun', 'home', 'other')),
  memo       text not null default '' check (char_length(memo) <= 40),
  created_at timestamptz not null default now()
);

create index if not exists entries_user_date on public.entries (user_id, date);

-- 行レベルセキュリティ: ログインした本人の行だけ読み書きできる
alter table public.entries enable row level security;

drop policy if exists "own rows: select" on public.entries;
drop policy if exists "own rows: insert" on public.entries;
drop policy if exists "own rows: delete" on public.entries;

create policy "own rows: select" on public.entries
  for select to authenticated using (auth.uid() = user_id);

create policy "own rows: insert" on public.entries
  for insert to authenticated with check (auth.uid() = user_id);

create policy "own rows: delete" on public.entries
  for delete to authenticated using (auth.uid() = user_id);
