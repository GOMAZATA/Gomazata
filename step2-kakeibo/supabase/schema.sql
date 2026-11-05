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

-- ---------- レシート読み取りの回数上限 ----------
-- 1人あたり1日（日本時間）に使える回数を数える表。中身は下の関数からしか触れない。
create table if not exists public.scan_usage (
  user_id uuid not null references auth.users (id) on delete cascade,
  day     date not null,
  count   integer not null default 0,
  primary key (user_id, day)
);

alter table public.scan_usage enable row level security;
-- ポリシーを作らない = ブラウザから直接は読み書きできない
revoke all on public.scan_usage from anon, authenticated;

-- 1回分を数えて、上限以内なら true を返す。上限を変えたいときは 20 を書き換えて Run し直す。
create or replace function public.claim_scan()
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  n integer;
begin
  if uid is null then
    return false;
  end if;
  insert into public.scan_usage (user_id, day, count)
  values (uid, (now() at time zone 'Asia/Tokyo')::date, 1)
  on conflict (user_id, day) do update set count = public.scan_usage.count + 1
  returning count into n;
  return n <= 20;
end;
$$;

revoke all on function public.claim_scan() from public, anon;
grant execute on function public.claim_scan() to authenticated;
