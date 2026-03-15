CREATE TABLE [users] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [tg_id] integer UNIQUE NOT NULL,
  [username] text,
  [first_name] text,
  [last_name] text,
  [source] text,
  [first_seen] timestamp,
  [last_seen] timestamp
)
GO

CREATE TABLE [states] (
  [user_id] integer PRIMARY KEY,
  [current_state] text,
  [data] text,
  [updated_at] timestamp
)
GO

CREATE TABLE [contacts] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [user_id] integer,
  [phone] text,
  [email] text,
  [collected_at] timestamp,
  [source_step] text
)
GO

CREATE TABLE [events] (
  [id] integer PRIMARY KEY IDENTITY(1, 1),
  [user_id] integer,
  [event_name] text,
  [event_data] text,
  [created_at] timestamp
)
GO

ALTER TABLE [states] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([tg_id])
GO

ALTER TABLE [contacts] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([tg_id])
GO

ALTER TABLE [events] ADD FOREIGN KEY ([user_id]) REFERENCES [users] ([tg_id])
GO
