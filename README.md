# icewall-community

- [x] Post와 Comment에 작성자 
    - [x] 작성자만 삭제할 수 있도록 조치 필요
    - [x] 변경된 session과 호응되도록 변경
    - [x] 게시글과 댓글에 작성자 이름 띄우기 
- [x] `/login/` 부분에 직접 `db`를 호출하지 않도록 
- [x] 회원가입, 로그인시 패스워드 암호화/복호화 과정 추가 
- [x] session에 username을 저장하는 게 아니라 세션키를 저장하도록 (`models.Session` 생성)
- [ ] 게시글이나 댓글 필터링 (XSS 방지)
    - [ ] 모든 사용자 입력 공간에 필터링 (유저네임도)
- [x] 서버에서 실행될 때 `debug` 끄기
- [ ] 로깅

- [ ] template
    - [ ] 에러 페이지 추가 
    - [x] 부트스트랩 적용 
    - [x] 에러 발생시 str만 리턴하는 게 아니라 메시지박스를 띄우도록 (flash, get_flashed_message 사용)
    - [x] `layout.html` 만들기 
