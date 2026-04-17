**TEXNIK TOPSHIRIQ (TZ)**
**Loyiha:** Ko‘p muallifli blog platformasi (Multi-Author / Publication Blog)
**Arxitektura:** Django MVT (faqat backend)
**Saqlash:** Local (`media/` papka)
**DB:** PostgreSQL (lekin boshlanishida SQLite ham mumkin)

---

# 1. UMUMIY TAVSIF

Bu tizimda bir nechta mualliflar (author) maqola yozadi, muharrirlar (editor) ularni tekshiradi va faqat tasdiqlangan maqolalar (published) saytga chiqadi.

---

# 2. APPLAR TUZILMASI (O‘ZBEKCHA)

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
* rol (ADMIN, MUHARRIR, MUALLIF) (index)
* is_active
* is_staff
* date_joined

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

* RegisterView (CreateView)
* LoginView
* LogoutView
* ProfileDetailView (DetailView)
* ProfileUpdateView (UpdateView)

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

# 4. MAQOLALAR APP (ASOSIY LOGIKA)

## Modellar

### Maqola (Post)

* id
* title (index)
* slug (unique, index)
* content
* author (FK → user, index)
* status (DRAFT, TEKSHIRUVDA, NASHR, ARXIV) (index)
* published_at (index)
* created_at
* updated_at
* view_count

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

### Muallif uchun:

* PostCreateView
* PostUpdateView
* PostListView (faqat o‘z maqolalari)
* PostDetailView

### Muharrir uchun:

* TekshiruvListView (status=TEKSHIRUVDA)
* PostTasdiqlashView
* PostRadEtishView

### Public:

* PublishedPostListView
* PublishedPostDetailView

---

## URLlar

```text
/posts/
/posts/<slug>/
/posts/create/
/posts/<slug>/edit/
/posts/my/
/posts/review/
/posts/<slug>/approve/
/posts/<slug>/reject/
```

---

# 5. KATEGORIYALAR APP

## Modellar

### Kategoriya

* id
* name (unique)
* slug (unique, index)

### Teg (Tag)

* id
* name (unique)
* slug (unique, index)

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
* post (FK, index)
* user (FK)
* content
* parent (self FK, nullable)
* is_approved (bool)
* created_at

### Like

* user (FK)
* post (FK)
* unique (user, post)

---

## Formalar

* IzohFormasi

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
* action (TASDIQLANDI, RAD_ETILDI)
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

## Vazifasi

* umumiy mixinlar
* helperlar
* base model

---

## Componentlar

### BaseModel

* created_at
* updated_at

### Mixinlar

* RoleRequiredMixin
* AuthorRequiredMixin
* EditorRequiredMixin

---

# 9. RUXSATLAR (PERMISSIONS)

### ADMIN

* hamma narsaga ruxsat

### MUHARRIR

* maqolani tasdiqlash/rad etish
* kategoriyalarni boshqarish

### MUALLIF

* faqat o‘z maqolalari bilan ishlaydi

---

# 10. MAQOLA HOLATLARI (WORKFLOW)

```text
MUALLIF:
DRAFT → TEKSHIRUVDA

MUHARRIR:
TEKSHIRUVDA → NASHR
TEKSHIRUVDA → DRAFT

SYSTEM:
NASHR → ARXIV
```

---

# 11. QIDIRUV

* title bo‘yicha search (icontains)
* kategoriya bo‘yicha filter
* teg bo‘yicha filter
* muallif bo‘yicha filter

---

# 12. CONCURRENCY (MUHIM)

Muammo:

* 2 ta user bir vaqtni o‘zida edit qilsa data yo‘qoladi

Yechim:

* PostRevision saqlash
* updated_at orqali tekshirish
* oxirgi tahrir validation

---

# 13. PERFORMANCE

## Indexlar

* Post.status
* Post.slug
* Post.author
* Post.published_at

---

## Optimizatsiya

* select_related(author)
* prefetch_related(tags, kategoriyalar)

---

# 14. PAGINATION

* har bir list view paginated (10–20)

---

# 15. MEDIA

* fayllar `media/` papkada saqlanadi
* upload_to:

  * users/
  * posts/

---

# 16. JAMOAVIY TAQSIMOT (3 DEVELOPER)

## XAZRATBEK (CORE + ARCHITECTURE + MAQOLALAR)

Mas’ul:

* asosiy app (mixinlar, base model)
* maqolalar app (Post, PostRevision)
* barcha maqola viewlari (CBV)
* workflow (DRAFT → NASHR)
* concurrency logic

Natija:

* butun loyiha yuragi (core logic)

---

## XOJIAKBAR (FOYDALANUVCHILAR + RUXSATLAR)

Mas’ul:

* kategoriyalar app
* izohlar app (comment + like)
* moderatsiya app
* search/filter logikasi

Natija:

* kontent struktura + interaction

---

## MUHAMMAD (KATEGORIYA + IZOH + MODERATSIYA)

Mas’ul:

* CustomUser modeli
* Profile modeli
* authentication (login/register)
* permission system (role-based)
* barcha user viewlari

Natija:

* xavfsizlik va access control

---

# 17. MVP TALABLARI

Majburiy:

* user system (role bilan)
* maqola yaratish/tahrirlash
* review system
* kategoriya/teg
* izohlar
* basic search

---

# FINAL

Agar shu TZ asosida yozilsa:

* real productionga yaqin tizim chiqadi

Agar noto‘g‘ri yozilsa:

* scalability yo‘q
* permission buziladi
* concurrency muammo beradi

Bu loyiha — oddiy blog emas.
To‘g‘ri qilsang, bu seni ishga olib kiradi.
