# OffGrid Platform — Database Schema

## Tables

### users
| Column    | Type    | Notes                          |
|-----------|---------|--------------------------------|
| id        | INTEGER | PK                             |
| name      | TEXT    |                                |
| email     | TEXT    | UNIQUE                         |
| password  | TEXT    | hashed (werkzeug)              |
| role      | TEXT    | student / organizer / sponsor  |
| branch    | TEXT    | CSE, IT, etc. (students)       |
| year      | INTEGER | 1-4 (students)                 |
| college   | TEXT    |                                |
| interests | TEXT    | comma-separated tags           |
| avatar    | TEXT    | 2-char initials                |
| created_at| DATETIME|                                |

### events
| Column       | Type    | Notes                                          |
|--------------|---------|------------------------------------------------|
| id           | INTEGER | PK                                             |
| title        | TEXT    |                                                |
| description  | TEXT    |                                                |
| category     | TEXT    | hackathon / workshop / cultural / seminar etc. |
| emoji        | TEXT    |                                                |
| date         | TEXT    | e.g. "Apr 18, 2025" or "TBD"                  |
| time         | TEXT    |                                                |
| venue        | TEXT    |                                                |
| capacity     | INTEGER |                                                |
| status       | TEXT    | draft / published / poll_active / cancelled    |
| tags         | TEXT    | comma-separated                                |
| organizer_id | INTEGER | FK → users.id                                  |
| club_name    | TEXT    |                                                |
| sponsor_name | TEXT    |                                                |
| created_at   | DATETIME|                                                |

### registrations
| Column    | Type    | Notes                       |
|-----------|---------|-----------------------------|
| id        | INTEGER | PK                          |
| user_id   | INTEGER | FK → users.id               |
| event_id  | INTEGER | FK → events.id              |
| status    | TEXT    | confirmed / waitlisted / cancelled |
| created_at| DATETIME|                             |
| UNIQUE(user_id, event_id)              |

### polls
| Column    | Type    | Notes                 |
|-----------|---------|-----------------------|
| id        | INTEGER | PK                    |
| event_id  | INTEGER | FK → events.id        |
| title     | TEXT    |                       |
| question  | TEXT    |                       |
| ends_at   | TEXT    |                       |
| status    | TEXT    | active / closed       |
| created_at| DATETIME|                       |

### poll_options
| Column  | Type    | Notes            |
|---------|---------|------------------|
| id      | INTEGER | PK               |
| poll_id | INTEGER | FK → polls.id    |
| label   | TEXT    |                  |
| votes   | INTEGER | running count    |

### votes
| Column    | Type    | Notes                        |
|-----------|---------|------------------------------|
| id        | INTEGER | PK                           |
| user_id   | INTEGER | FK → users.id                |
| option_id | INTEGER | FK → poll_options.id         |
| poll_id   | INTEGER |                              |
| UNIQUE(user_id, poll_id)                   |

### proposals
| Column     | Type    | Notes                                    |
|------------|---------|------------------------------------------|
| id         | INTEGER | PK                                       |
| sponsor_id | INTEGER | FK → users.id                            |
| event_id   | INTEGER | FK → events.id                           |
| amount     | TEXT    | e.g. "₹15,000"                          |
| perks      | TEXT    |                                          |
| message    | TEXT    |                                          |
| status     | TEXT    | pending / accepted / rejected / discussing|
| created_at | DATETIME|                                          |

### reviews
| Column    | Type    | Notes                 |
|-----------|---------|-----------------------|
| id        | INTEGER | PK                    |
| user_id   | INTEGER | FK → users.id         |
| event_id  | INTEGER | FK → events.id        |
| rating    | INTEGER | 1-5                   |
| comment   | TEXT    |                       |
| created_at| DATETIME|                       |
| UNIQUE(user_id, event_id)              |