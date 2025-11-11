# Django 블로그 웹 애플리케이션 API 설계

## 목차
1. [Main App API](#main-app-api)
2. [Accounts App API](#accounts-app-api)
3. [Blog App API](#blog-app-api)
4. [API 상세 설계](#api-상세-설계)

---

## Main App API

### 1. 메인 페이지
- **URL**: `/`
- **Method**: GET
- **View**: `HomeView` (TemplateView)
- **Template**: `templates/main/home.html`
- **권한**: 누구나 접근 가능
- **설명**: 블로그의 메인 랜딩 페이지

### 2. 소개 페이지
- **URL**: `/about/`
- **Method**: GET
- **View**: `AboutView` (TemplateView)
- **Template**: `templates/main/about.html`
- **권한**: 누구나 접근 가능
- **설명**: 블로그 및 기능 소개 페이지

### 3. 연락처 페이지
- **URL**: `/contact/`
- **Method**: GET
- **View**: `ContactView` (TemplateView)
- **Template**: `templates/main/contact.html`
- **권한**: 누구나 접근 가능
- **설명**: 연락처 정보 표시 페이지

---

## Accounts App API

### 1. 회원가입
- **URL**: `/accounts/signup/`
- **Method**: GET, POST
- **View**: `SignUpView` (CreateView)
- **Template**: `templates/accounts/signup.html`
- **권한**: 비로그인 사용자만 접근 가능
- **Form**: `UserCreationForm`
- **Success URL**: `/accounts/login/`
- **설명**:
  - GET: 회원가입 폼 표시
  - POST: 회원가입 처리 및 로그인 페이지로 리다이렉트

### 2. 로그인
- **URL**: `/accounts/login/`
- **Method**: GET, POST
- **View**: `LoginView` (Django의 LoginView 상속)
- **Template**: `templates/accounts/login.html`
- **권한**: 비로그인 사용자만 접근 가능
- **Redirect**: `LOGIN_REDIRECT_URL` (기본값: `/`)
- **설명**:
  - GET: 로그인 폼 표시
  - POST: 로그인 처리 및 메인 페이지로 리다이렉트
  - `redirect_authenticated_user=True`: 이미 로그인된 사용자는 자동으로 메인 페이지로 리다이렉트

### 3. 로그아웃
- **URL**: `/accounts/logout/`
- **Method**: GET, POST
- **View**: `LogoutView` (Django의 LogoutView 상속)
- **권한**: 로그인 사용자만 접근 가능
- **Redirect**: `LOGOUT_REDIRECT_URL` (기본값: `/`)
- **설명**: 로그아웃 처리 및 메인 페이지로 리다이렉트

---

## Blog App API

### 1. 블로그 글 목록
- **URL**: `/blog/`
- **Query Parameter**: `?search=<str:query>` (선택사항)
- **Method**: GET
- **View**: `PostListView` (ListView)
- **Template**: `templates/blog/post_list.html`
- **권한**: 누구나 접근 가능
- **Pagination**: 페이지당 10개 게시글
- **설명**:
  - 공개된 게시글 목록 표시 (is_published=True)
  - 검색 기능 지원 (제목 및 내용 검색)
  - 모든 태그 목록 표시
  - 최신 게시글부터 표시 (생성일 역순)

### 2. 블로그 글 상세
- **URL**: `/blog/<int:pk>/`
- **Method**: GET
- **View**: `PostDetailView` (DetailView)
- **Template**: `templates/blog/post_detail.html`
- **권한**: 누구나 접근 가능 (공개된 게시글만)
- **설명**:
  - 게시글 상세 내용 표시 (마크다운 렌더링)
  - 게시글에 달린 댓글 목록 표시
  - 로그인한 사용자에게 댓글 작성 폼 제공
  - 작성자에게 수정/삭제 버튼 표시

### 3. 블로그 글 생성
- **URL**: `/blog/create/`
- **Method**: GET, POST
- **View**: `PostCreateView` (CreateView)
- **Template**: `templates/blog/post_form.html`
- **권한**: 로그인 사용자만 접근 가능 (LoginRequiredMixin)
- **Form**: `PostForm`
- **Success URL**: 생성된 게시글 상세 페이지
- **설명**:
  - GET: 게시글 작성 폼 표시
  - POST: 게시글 생성 및 상세 페이지로 리다이렉트
  - 작성자는 자동으로 현재 로그인한 사용자로 설정

### 4. 블로그 글 수정
- **URL**: `/blog/<int:pk>/update/`
- **Method**: GET, POST
- **View**: `PostUpdateView` (UpdateView)
- **Template**: `templates/blog/post_form.html`
- **권한**: 게시글 작성자만 접근 가능 (LoginRequiredMixin, UserPassesTestMixin)
- **Form**: `PostForm`
- **Success URL**: 수정된 게시글 상세 페이지
- **설명**:
  - GET: 게시글 수정 폼 표시 (기존 내용 포함)
  - POST: 게시글 수정 및 상세 페이지로 리다이렉트
  - 작성자가 아닌 사용자가 접근 시 403 에러

### 5. 블로그 글 삭제
- **URL**: `/blog/<int:pk>/delete/`
- **Method**: GET, POST
- **View**: `PostDeleteView` (DeleteView)
- **Template**: `templates/blog/post_confirm_delete.html`
- **권한**: 게시글 작성자만 접근 가능 (LoginRequiredMixin, UserPassesTestMixin)
- **Success URL**: `/blog/` (게시글 목록)
- **설명**:
  - GET: 삭제 확인 페이지 표시
  - POST: 게시글 삭제 및 게시글 목록으로 리다이렉트
  - 작성자가 아닌 사용자가 접근 시 403 에러

### 6. 댓글 생성
- **URL**: `/blog/<int:post_pk>/comment/create/`
- **Method**: POST
- **View**: `CommentCreateView` (CreateView)
- **권한**: 로그인 사용자만 접근 가능 (LoginRequiredMixin)
- **Form**: `CommentForm`
- **Success URL**: 댓글이 달린 게시글 상세 페이지
- **설명**:
  - POST only (GET 요청 불가)
  - 댓글 작성 및 게시글 상세 페이지로 리다이렉트
  - 작성자와 게시글은 자동으로 설정

### 7. 댓글 수정
- **URL**: `/blog/comment/<int:pk>/update/`
- **Method**: GET, POST
- **View**: `CommentUpdateView` (UpdateView)
- **Template**: `templates/blog/comment_form.html`
- **권한**: 댓글 작성자만 접근 가능 (LoginRequiredMixin, UserPassesTestMixin)
- **Form**: `CommentForm`
- **Success URL**: 댓글이 달린 게시글 상세 페이지
- **설명**:
  - GET: 댓글 수정 폼 표시
  - POST: 댓글 수정 및 게시글 상세 페이지로 리다이렉트
  - 작성자가 아닌 사용자가 접근 시 403 에러

### 8. 댓글 삭제
- **URL**: `/blog/comment/<int:pk>/delete/`
- **Method**: GET, POST
- **View**: `CommentDeleteView` (DeleteView)
- **Template**: `templates/blog/comment_confirm_delete.html`
- **권한**: 댓글 작성자만 접근 가능 (LoginRequiredMixin, UserPassesTestMixin)
- **Success URL**: 댓글이 달린 게시글 상세 페이지
- **설명**:
  - GET: 삭제 확인 페이지 표시
  - POST: 댓글 삭제 및 게시글 상세 페이지로 리다이렉트
  - 작성자가 아닌 사용자가 접근 시 403 에러

### 9. Tag 검색
- **URL**: `/blog/tag/<str:slug>/`
- **Method**: GET
- **View**: `PostByTagListView` (ListView)
- **Template**: `templates/blog/post_list_by_tag.html`
- **권한**: 누구나 접근 가능
- **Pagination**: 페이지당 10개 게시글
- **설명**:
  - 특정 태그를 가진 게시글 목록 표시
  - 태그가 존재하지 않으면 404 에러
  - 공개된 게시글만 표시 (is_published=True)

### 10. Title 검색
- **URL**: `/blog/?search=<str:query>`
- **Method**: GET
- **View**: `PostListView` (ListView) - 검색 쿼리 처리
- **Template**: `templates/blog/post_list.html`
- **권한**: 누구나 접근 가능
- **설명**:
  - 게시글 제목 또는 내용에 검색어 포함된 게시글 목록 표시
  - 검색어가 없으면 전체 게시글 목록 표시
  - 공개된 게시글만 표시 (is_published=True)

---

## API 상세 설계

### URL 네임스페이스 구조
```
main:
  - home
  - about
  - contact
  - post_list
  - post_detail
  - post_create
  - post_update
  - post_delete
  - post_by_tag
  - comment_create
  - comment_update
  - comment_delete

accounts:
  - signup
  - login
  - logout
```

### HTTP Method별 동작
| API | GET | POST | 설명 |
|-----|-----|------|------|
| `/` | 메인 페이지 표시 | - | TemplateView |
| `/about/` | 소개 페이지 표시 | - | TemplateView |
| `/contact/` | 연락처 페이지 표시 | - | TemplateView |
| `/accounts/signup/` | 회원가입 폼 표시 | 회원가입 처리 | CreateView |
| `/accounts/login/` | 로그인 폼 표시 | 로그인 처리 | LoginView |
| `/accounts/logout/` | 로그아웃 처리 | 로그아웃 처리 | LogoutView |
| `/blog/` | 게시글 목록 표시 | - | ListView |
| `/blog/<int:pk>/` | 게시글 상세 표시 | - | DetailView |
| `/blog/create/` | 게시글 작성 폼 표시 | 게시글 생성 | CreateView |
| `/blog/<int:pk>/update/` | 게시글 수정 폼 표시 | 게시글 수정 | UpdateView |
| `/blog/<int:pk>/delete/` | 삭제 확인 페이지 표시 | 게시글 삭제 | DeleteView |
| `/blog/<int:post_pk>/comment/create/` | - | 댓글 생성 | CreateView (POST only) |
| `/blog/comment/<int:pk>/update/` | 댓글 수정 폼 표시 | 댓글 수정 | UpdateView |
| `/blog/comment/<int:pk>/delete/` | 삭제 확인 페이지 표시 | 댓글 삭제 | DeleteView |
| `/blog/tag/<str:slug>/` | 태그별 게시글 목록 표시 | - | ListView |

### 권한 체계
| 권한 레벨 | 적용 URL | Mixin |
|----------|---------|--------|
| 누구나 | `/`, `/about/`, `/contact/`, `/blog/`, `/blog/<pk>/`, `/blog/tag/<slug>/` | - |
| 로그인 필요 | `/blog/create/`, `/blog/<post_pk>/comment/create/` | LoginRequiredMixin |
| 작성자만 | `/blog/<pk>/update/`, `/blog/<pk>/delete/`, `/blog/comment/<pk>/update/`, `/blog/comment/<pk>/delete/` | LoginRequiredMixin, UserPassesTestMixin |

### 리다이렉트 정책
| 상황 | 리다이렉트 URL |
|------|---------------|
| 로그인 성공 | `/` (LOGIN_REDIRECT_URL) |
| 로그아웃 | `/` (LOGOUT_REDIRECT_URL) |
| 회원가입 성공 | `/accounts/login/` |
| 게시글 생성 성공 | `/blog/<pk>/` (생성된 게시글 상세) |
| 게시글 수정 성공 | `/blog/<pk>/` (수정된 게시글 상세) |
| 게시글 삭제 성공 | `/blog/` (게시글 목록) |
| 댓글 생성 성공 | `/blog/<post_pk>/` (댓글이 달린 게시글 상세) |
| 댓글 수정 성功 | `/blog/<post_pk>/` (댓글이 달린 게시글 상세) |
| 댓글 삭제 성공 | `/blog/<post_pk>/` (댓글이 달린 게시글 상세) |
| 비로그인 사용자가 로그인 필요 페이지 접근 | `/accounts/login/?next=<requested_url>` |

### Context 데이터
| View | Context 변수명 | 설명 |
|------|---------------|------|
| PostListView | `posts` | 게시글 목록 |
| PostListView | `page_obj` | 페이지네이션 객체 |
| PostDetailView | `post` | 게시글 객체 |
| PostDetailView | `comment_form` | 댓글 작성 폼 |
| PostByTagListView | `posts` | 게시글 목록 |
| PostByTagListView | `tag` | 현재 태그 객체 |
| PostByTagListView | `page_obj` | 페이지네이션 객체 |

---

## 에러 처리
| 상황 | HTTP 상태 코드 | 설명 |
|------|---------------|------|
| 존재하지 않는 게시글/댓글 | 404 Not Found | get_object_or_404 사용 |
| 권한 없는 사용자의 수정/삭제 시도 | 403 Forbidden | UserPassesTestMixin의 test_func 실패 |
| 비로그인 사용자의 로그인 필요 페이지 접근 | 302 Redirect | LOGIN_URL로 리다이렉트 |
| 존재하지 않는 태그 | 404 Not Found | get_object_or_404 사용 |

---

## 완료!
이 API 설계서는 Django CBV를 사용한 블로그 웹 애플리케이션의 모든 엔드포인트를 정의합니다.
