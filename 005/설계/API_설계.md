# Django 블로그 API 설계 문서

## 목차
1. [인증 관련 API](#인증-관련-api)
2. [게시글 관련 API](#게시글-관련-api)
3. [댓글 관련 API](#댓글-관련-api)
4. [태그 관련 API](#태그-관련-api)

---

## 인증 관련 API

### 1. 회원가입
- **URL**: `/accounts/signup/`
- **Method**: `GET`, `POST`
- **View**: `SignUpView` (CreateView)
- **기능**:
  - GET: 회원가입 폼 표시
  - POST: 새로운 사용자 계정 생성
- **필수 입력 필드**:
  - username (사용자명)
  - email (이메일)
  - password1 (비밀번호)
  - password2 (비밀번호 확인)
- **성공 시**: 로그인 페이지로 리다이렉트
- **실패 시**: 에러 메시지와 함께 회원가입 폼 재표시

### 2. 로그인
- **URL**: `/accounts/login/`
- **Method**: `GET`, `POST`
- **View**: `LoginView` (내장 LoginView)
- **기능**:
  - GET: 로그인 폼 표시
  - POST: 사용자 인증 및 세션 생성
- **필수 입력 필드**:
  - username (사용자명)
  - password (비밀번호)
- **성공 시**: 홈 페이지 또는 next 파라미터로 지정된 페이지로 리다이렉트
- **실패 시**: 에러 메시지와 함께 로그인 폼 재표시

### 3. 로그아웃
- **URL**: `/accounts/logout/`
- **Method**: `POST`
- **View**: `LogoutView` (내장 LogoutView)
- **기능**: 현재 사용자의 세션 종료
- **인증 요구**: 로그인된 사용자만 접근 가능
- **성공 시**: 홈 페이지로 리다이렉트

---

## 게시글 관련 API

### 1. 게시글 목록 조회
- **URL**: `/blog/`
- **Method**: `GET`
- **View**: `PostListView` (ListView)
- **기능**: 공개된 게시글 목록 조회 (최신순 정렬)
- **쿼리 파라미터**:
  - `page`: 페이지 번호 (기본값: 1)
- **응답 데이터**:
  - 게시글 목록 (제목, 작성자, 작성일, 태그)
  - 페이지네이션 정보
- **인증 요구**: 없음

### 2. 게시글 상세 조회
- **URL**: `/blog/<int:pk>/`
- **Method**: `GET`
- **View**: `PostDetailView` (DetailView)
- **기능**: 특정 게시글의 상세 내용 조회 (마크다운 렌더링)
- **응답 데이터**:
  - 게시글 상세 정보 (제목, 내용, 작성자, 작성일, 수정일, 태그)
  - 연결된 댓글 목록
- **인증 요구**: 없음 (공개 게시글만)

### 3. 게시글 작성
- **URL**: `/blog/create/`
- **Method**: `GET`, `POST`
- **View**: `PostCreateView` (CreateView)
- **기능**:
  - GET: 게시글 작성 폼 표시
  - POST: 새로운 게시글 생성
- **필수 입력 필드**:
  - title (제목)
  - content (내용, 마크다운 지원)
- **선택 입력 필드**:
  - tags (태그, 다중 선택)
  - is_published (공개 여부)
- **인증 요구**: 로그인된 사용자만 접근 가능
- **성공 시**: 생성된 게시글 상세 페이지로 리다이렉트

### 4. 게시글 수정
- **URL**: `/blog/<int:pk>/update/`
- **Method**: `GET`, `POST`
- **View**: `PostUpdateView` (UpdateView)
- **기능**:
  - GET: 게시글 수정 폼 표시 (기존 데이터 자동 입력)
  - POST: 게시글 수정 내용 저장
- **수정 가능 필드**:
  - title (제목)
  - content (내용, 마크다운 지원)
  - tags (태그)
  - is_published (공개 여부)
- **인증 요구**: 게시글 작성자만 수정 가능
- **성공 시**: 수정된 게시글 상세 페이지로 리다이렉트

### 5. 게시글 삭제
- **URL**: `/blog/<int:pk>/delete/`
- **Method**: `GET`, `POST`
- **View**: `PostDeleteView` (DeleteView)
- **기능**:
  - GET: 삭제 확인 페이지 표시
  - POST: 게시글 삭제
- **인증 요구**: 게시글 작성자만 삭제 가능
- **성공 시**: 게시글 목록 페이지로 리다이렉트

---

## 댓글 관련 API

### 1. 댓글 작성
- **URL**: `/blog/<int:post_pk>/comment/create/`
- **Method**: `POST`
- **View**: `CommentCreateView` (CreateView)
- **기능**: 특정 게시글에 댓글 작성
- **필수 입력 필드**:
  - content (댓글 내용)
- **인증 요구**: 로그인된 사용자만 작성 가능
- **성공 시**: 게시글 상세 페이지로 리다이렉트

### 2. 댓글 수정
- **URL**: `/blog/comment/<int:pk>/update/`
- **Method**: `GET`, `POST`
- **View**: `CommentUpdateView` (UpdateView)
- **기능**:
  - GET: 댓글 수정 폼 표시
  - POST: 댓글 수정 내용 저장
- **수정 가능 필드**:
  - content (댓글 내용)
- **인증 요구**: 댓글 작성자만 수정 가능
- **성공 시**: 게시글 상세 페이지로 리다이렉트

### 3. 댓글 삭제
- **URL**: `/blog/comment/<int:pk>/delete/`
- **Method**: `POST`
- **View**: `CommentDeleteView` (DeleteView)
- **기능**: 댓글 삭제
- **인증 요구**: 댓글 작성자만 삭제 가능
- **성공 시**: 게시글 상세 페이지로 리다이렉트

---

## 태그 관련 API

### 1. 특정 태그의 게시글 목록
- **URL**: `/blog/tag/<str:slug>/`
- **Method**: `GET`
- **View**: `PostByTagListView` (ListView)
- **기능**: 특정 태그가 연결된 게시글 목록 조회
- **응답 데이터**:
  - 태그 정보
  - 해당 태그의 게시글 목록
  - 페이지네이션 정보
- **인증 요구**: 없음

---

## 공통 응답 규칙

### 성공 응답
- **게시글/댓글 생성, 수정**: 해당 리소스 페이지로 리다이렉트
- **게시글/댓글 삭제**: 목록 페이지로 리다이렉트

### 에러 응답
- **400 Bad Request**: 잘못된 입력 데이터
- **401 Unauthorized**: 인증되지 않은 사용자
- **403 Forbidden**: 권한 없음 (타인의 게시글/댓글 수정/삭제 시도)
- **404 Not Found**: 존재하지 않는 리소스

---

## URL 전체 구조

```
# 홈 & 기본 페이지
/ : 홈 페이지
/about/ : 소개 페이지
/contact/ : 연락처 페이지

# 인증
/accounts/signup/ : 회원가입
/accounts/login/ : 로그인
/accounts/logout/ : 로그아웃

# 게시글
/blog/ : 게시글 목록
/blog/create/ : 게시글 작성
/blog/<int:pk>/ : 게시글 상세
/blog/<int:pk>/update/ : 게시글 수정
/blog/<int:pk>/delete/ : 게시글 삭제

# 댓글
/blog/<int:post_pk>/comment/create/ : 댓글 작성
/blog/comment/<int:pk>/update/ : 댓글 수정
/blog/comment/<int:pk>/delete/ : 댓글 삭제

# 태그
/blog/tag/<str:slug>/ : 특정 태그 게시글 목록

# 관리자
/admin/ : 관리자 페이지
```

---

## 참고사항

1. **마크다운 지원**: 게시글 내용은 마크다운 형식으로 작성 가능하며, 표시 시 HTML로 렌더링됩니다.
2. **페이지네이션**: 게시글 목록은 페이지당 10개씩 표시됩니다.
3. **권한 관리**:
   - 게시글/댓글 작성: 로그인 필요
   - 게시글/댓글 수정/삭제: 작성자만 가능
4. **CSRF 보호**: 모든 POST, PUT, DELETE 요청은 CSRF 토큰 필요
