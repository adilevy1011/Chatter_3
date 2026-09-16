SET local check_function_bodies = off;

CREATE TABLE "public"."ai_chat_messages" (
  "id"                uuid                     NOT NULL DEFAULT gen_random_uuid(),
  "thread_id"         uuid                     NOT NULL,
  "user_message"      text                     NOT NULL,
  "created_at"        timestamp with time zone NOT NULL DEFAULT now(),
  "assistant_message" text,
  "ai_thinking"       text,
  CONSTRAINT "ai_chat_messages_pkey" PRIMARY KEY (id),
  "user_id"           uuid                     NOT NULL DEFAULT auth.uid()
);

ALTER TABLE "public"."ai_chat_messages"
  ENABLE ROW LEVEL SECURITY;

CREATE TABLE "public"."ai_chat_threads" (
  "id"           uuid                     NOT NULL DEFAULT gen_random_uuid(),
  "created_at"   timestamp with time zone NOT NULL DEFAULT now(),
  "updated_at"   timestamp with time zone NOT NULL DEFAULT now(),
  "thread_title" text,
  CONSTRAINT "ai_chat_threads_pkey" PRIMARY KEY (id),
  "user_id"      uuid                     NOT NULL DEFAULT auth.uid()
);

ALTER TABLE "public"."ai_chat_threads"
  ENABLE ROW LEVEL SECURITY;

CREATE TABLE "public"."healthcheck" (
  "id" uuid
);

ALTER TABLE "public"."healthcheck"
  ENABLE ROW LEVEL SECURITY;

CREATE TABLE "public"."profiles" (
  "id"         uuid                     NOT NULL,
  "username"   text,
  "full_name"  text,
  "avatar_url" text,
  "updated_at" timestamp with time zone,
  "created_at" timestamp with time zone DEFAULT now(),
  "email"      text,
  CONSTRAINT "profiles_pkey" PRIMARY KEY (id),
  CONSTRAINT "profiles_username_key" UNIQUE (username)
);

ALTER TABLE "public"."profiles"
  ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION public.rls_auto_enable()
  RETURNS event_trigger
  LANGUAGE plpgsql
  SECURITY DEFINER
  SET search_path TO 'pg_catalog'
  AS $function$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN
    SELECT *
    FROM pg_event_trigger_ddl_commands()
    WHERE command_tag IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')
      AND object_type IN ('table','partitioned table')
  LOOP
     IF cmd.schema_name IS NOT NULL AND cmd.schema_name IN ('public') AND cmd.schema_name NOT IN ('pg_catalog','information_schema') AND cmd.schema_name NOT LIKE 'pg_toast%' AND cmd.schema_name NOT LIKE 'pg_temp%' THEN
      BEGIN
        EXECUTE format('alter table if exists %s enable row level security', cmd.object_identity);
        RAISE LOG 'rls_auto_enable: enabled RLS on %', cmd.object_identity;
      EXCEPTION
        WHEN OTHERS THEN
          RAISE LOG 'rls_auto_enable: failed to enable RLS on %', cmd.object_identity;
      END;
     ELSE
        RAISE LOG 'rls_auto_enable: skip % (either system schema or not in enforced list: %.)', cmd.object_identity, cmd.schema_name;
     END IF;
  END LOOP;
END;
$function$;

ALTER TABLE "public"."ai_chat_messages"
  ADD CONSTRAINT "ai_chat_messages_thread_id_fkey" FOREIGN KEY (thread_id) REFERENCES public.ai_chat_threads(id) ON DELETE CASCADE;

ALTER TABLE "public"."profiles"
  ADD CONSTRAINT "profiles_id_fkey" FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;

CREATE INDEX idx_ai_chat_messages_thread_id ON public.ai_chat_messages USING btree (thread_id, created_at DESC);

CREATE POLICY "Users can update their own profile." ON "public"."profiles"
  FOR UPDATE
  TO PUBLIC
  USING ((auth.uid() = id));

CREATE POLICY "Users can view their own profile." ON "public"."profiles"
  FOR SELECT
  TO PUBLIC
  USING ((auth.uid() = id));

CREATE POLICY "users can insert their own profiles" ON "public"."profiles"
  FOR ALL
  TO "authenticated"
  WITH CHECK ((auth.uid() = id));

CREATE EVENT TRIGGER "ensure_rls"
  ON ddl_command_end
  WHEN TAG IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')
  EXECUTE FUNCTION "public"."rls_auto_enable"();

GRANT EXECUTE ON FUNCTION "public"."rls_auto_enable"() TO PUBLIC, "anon", "authenticated", "postgres", "service_role";

GRANT DELETE, INSERT, MAINTAIN, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON TABLE "public"."ai_chat_messages" TO "anon", "authenticated", "postgres", "service_role";

GRANT DELETE, INSERT, MAINTAIN, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON TABLE "public"."ai_chat_threads" TO "anon", "authenticated", "postgres", "service_role";

GRANT DELETE, INSERT, MAINTAIN, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON TABLE "public"."healthcheck" TO "anon", "authenticated", "postgres", "service_role";

GRANT DELETE, INSERT, MAINTAIN, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON TABLE "public"."profiles" TO "anon", "authenticated", "postgres", "service_role";

ALTER TABLE "public"."ai_chat_messages"
  ADD CONSTRAINT "ai_chat_messages_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

CREATE POLICY "users can insert their own ai chat messages" ON "public"."ai_chat_messages"
  FOR INSERT
  TO "authenticated"
  WITH CHECK ((auth.uid() = user_id));

CREATE POLICY "users can update their own ai chat messages" ON "public"."ai_chat_messages"
  FOR UPDATE
  TO "authenticated"
  USING ((( SELECT auth.uid() AS uid) = user_id))
  WITH CHECK ((( SELECT auth.uid() AS uid) = user_id));

CREATE POLICY "users can view their own ai chat messages" ON "public"."ai_chat_messages"
  FOR SELECT
  TO "authenticated"
  USING ((user_id = auth.uid()));

ALTER TABLE "public"."ai_chat_threads"
  ADD CONSTRAINT "ai_chat_threads_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

CREATE POLICY "users can insert their own ai chat threads" ON "public"."ai_chat_threads"
  FOR INSERT
  TO "authenticated"
  WITH CHECK ((auth.uid() = user_id));

CREATE POLICY "users can update their own ai chat threads" ON "public"."ai_chat_threads"
  FOR UPDATE
  TO "authenticated"
  USING ((( SELECT auth.uid() AS uid) = user_id))
  WITH CHECK ((( SELECT auth.uid() AS uid) = user_id));

CREATE POLICY "users can view their own ai chat threads" ON "public"."ai_chat_threads"
  FOR SELECT
  TO "authenticated"
  USING ((user_id = auth.uid()));

