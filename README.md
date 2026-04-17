**TEXNIK TOPSHIRIQ (TZ)**
**Loyiha:** Ko‘p muallifli blog platformasi (Multi-Author / Publication Blog)
**Arxitektura:** Django MVT (faqat backend)
**Saqlash:** Local (`media/` papka)
**DB:** PostgreSQL (boshlanishda SQLite mumkin)

---

# 1. UMUMIY TAVSIF

Bu tizimda bir nechta mualliflar maqola yozadi.
Maqola faqat **ADMIN tekshirganidan keyin** saytga chiqadi.

👉 Workflow qat’iy:

* MUALLIF yozadi
* ADMIN tekshiradi
* ADMIN tasdiqlasa → PUBLISHED bo‘ladi

---

# 2. APPLAR TUZILMASI

```text
- foydalanuvchilar
- asosiy
- maqolalar
- kategoriyalar
- izohlar
- moderatsiya
```

---

# 3. FOYDALANUVCHILAR APP

## Modellar

### Foydalanuvchi (CustomUser)

* id
* username (unique, index)
* email (unique, index)
* rol (ADMIN, MUALLIF) (index)
* is_active
* is_staff
* date_joined

👉 MUHIM: Editor YO‘Q

---

### Profil

* user (OneToOne)
* bio
* avatar (upload_to='users/')
* website

---

## Formalar

* FoydalanuvchiYaratishFormasi
* ProfilYangilashFormasi

---

## Viewlar (CBV)

* RegisterView
* LoginView
* LogoutView
* ProfileDetailView
* ProfileUpdateView

---

## URLlar

```text
/accounts/register/
/accounts/login/
/accounts/logout/
/accounts/profile/<username>/
/accounts/profile/edit/
```

---

# 4. MAQOLALAR APP (CORE)

## Modellar

### Maqola (Post)

* id
* title (index)
* slug (unique, index)
* content
* author (FK → user, index)
* status (DRAFT, TEKSHIRUVDA, PUBLISHED, ARXIV) (index)
* published_at (index)
* created_at
* updated_at
* view_count

👉 STATUS LOGIC:

* DRAFT → TEKSHIRUVDA (muallif yuboradi)
* TEKSHIRUVDA → PUBLISHED (faqat ADMIN)
* TEKSHIRUVDA → DRAFT (ADMIN rad etsa)
* PUBLISHED → ARXIV (system/ADMIN)

---

### MaqolaTahriri (PostRevision)

* post (FK)
* content_snapshot
* edited_by (FK user)
* created_at

---

## Formalar

* MaqolaYaratishFormasi
* MaqolaTahrirlashFormasi

---

## Viewlar (CBV)

### MUALLIF

* PostCreateView
* PostUpdateView
* PostListView (o‘z maqolalari)
* PostDetailView
* PostSubmitForReviewView (DRAFT → TEKSHIRUVDA)

---

### ADMIN

* ReviewListView (TEKSHIRUVDA status)
* PostPublishView (TEKSHIRUVDA → PUBLISHED)
* PostRejectView (TEKSHIRUVDA → DRAFT)

---

### PUBLIC

* PublishedPostListView (faqat PUBLISHED)
* PublishedPostDetailView

---

## URLlar

```text
/posts/
/posts/<slug>/
/posts/create/
/posts/<slug>/edit/
/posts/my/
/posts/submit/<slug>/
/posts/review/
/posts/<slug>/publish/
/posts/<slug>/reject/
```

---

# 5. KATEGORIYALAR APP

## Modellar

### Kategoriya

* id
* name
* slug

### Teg

* id
* name
* slug

### PostKategoriya

* post
* kategoriya

### PostTeg

* post
* teg

---

## Viewlar

* CategoryListView
* CategoryDetailView
* TagDetailView

---

## URLlar

```text
/categories/
/categories/<slug>/
/tags/<slug>/
```

---

# 6. IZOHLAR APP

## Modellar

### Izoh

* id
* post (FK)
* user (FK)
* content
* parent (self FK)
* is_approved
* created_at

### Like

* user
* post
* unique(user, post)

---

## Viewlar

* CommentCreateView
* CommentDeleteView
* LikeToggleView

---

## URLlar

```text
/posts/<slug>/comment/
/comments/<id>/delete/
/posts/<slug>/like/
```

---

# 7. MODERATSIYA APP

## Modellar

### ModeratsiyaLog

* post
* action (PUBLISHED, REJECTED)
* performed_by
* note
* created_at

### Shikoyat (Flag)

* post
* user
* reason
* created_at

---

## Viewlar

* FlagCreateView
* ModeratsiyaLogListView

---

## URLlar

```text
/moderation/flags/
/moderation/logs/
```

---

# 8. ASOSIY APP

## Vazifa

* umumiy mixinlar
* base model
* helperlar

---

## BaseModel

* created_at
* updated_at

---

## Mixinlar

* RoleRequiredMixin
* AuthorQuerysetMixin

---

# 9. RUXSATLAR

### ADMIN

* hamma narsaga ruxsat
* maqolani publish/reject qiladi

### MUALLIF

* maqola yozadi
* reviewga yuboradi
* faqat o‘z postlari

---

# 10. WORKFLOW (ENG MUHIM QISM)

```text
MUALLIF:
DRAFT → TEKSHIRUVDA

ADMIN:
TEKSHIRUVDA → PUBLISHED
TEKSHIRUVDA → DRAFT

SYSTEM:
PUBLISHED → ARXIV
```

---

# 11. QIDIRUV

* title (icontains)
* category filter
* tag filter
* author filter

---

# 12. CONCURRENCY

* PostRevision saqlanadi
* updated_at check
* overwrite protection

---

# 13. PERFORMANCE

## Indexlar

* Post.status
* Post.slug
* Post.author
* Post.published_at

---

## Optimisation

* select_related(author)
* prefetch_related(tags, categories)

---

# 14. PAGINATION

* har bir list view: 10–20 item

---

# 15. MEDIA

* media/users/
* media/posts/

---

# 16. JAMOAVIY TAQSIMOT

## XAZRATBEK (CORE + MAQOLALAR)

* maqolalar app
* Post modeli
* workflow logic
* review system
* post views

👉 loyihaning yuragi

---

## XOJIAKBAR (KATEGORIYA + IZOH + MODERATSIYA)

* categories app
* comments app
* likes
* moderation system

👉 interaction layer

---

## MUHAMMAD (FOYDALANUVCHI + RUXSAT)

* CustomUser
* Profile
* login/register
* permissions (ADMIN / MUALLIF)
* auth system

👉 security layer

---

# 17. MVP TALABLARI

Majburiy:

* user system
* post CRUD
* submit for review
* admin publish/reject
* categories/tags
* comments
* basic search

---

# FINAL

Bu loyiha:

* editor yo‘q
* faqat ADMIN control
* simple workflow
* lekin real production architecture

👉 To‘g‘ri qilinsa: portfolio darajasi yuqori bo‘ladi
👉 Noto‘g‘ri qilinsa: oddiy CRUD blog bo‘lib qoladi
