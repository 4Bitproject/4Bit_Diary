# 4Bit_Diary-
4Bit팀의 Diary만드는 Project
<img width="1995" height="616" alt="스크린샷 2025-08-27 오후 1 03 20" src="https://github.com/user-attachments/assets/4e8757a9-f944-4ecc-963a-2d0417c753ef" />

```mermaid
 flowchart TD
 %% 회원가입
    A1[회원가입] --> A2[DB에 사용자 저장]

    %% 로그인
    A2 --> B1[로그인]
    B1 --> B2[Access Token + Refresh Token 발급]

    %% API 요청
    B2 --> C1[Access Token으로 API 호출]
    C1 --> C2{Access Token 유효?}
    C2 -- 예 --> C3[정상 처리]
    C2 -- 아니오 --> D1[토큰 재발급 요청]

    %% 토큰 재발급
    D1 --> D2{Refresh Token 유효?}
    D2 -- 예 --> D3[새 Access Token 발급]
    D3 --> C1
    D2 -- 아니오 --> B1[다시 로그인 필요]

    %% 로그아웃
    B2 --> E1[로그아웃 요청]
    E1 --> E2[Refresh Token 무효화]
    E2 --> B1[로그인 단계로 되돌아감]

```
## 인증 흐름 요약

- **회원가입 (`/signup`)** → 사용자 정보를 DB에 저장하고 가입 완료 응답  
- **로그인 (`/login`)** → 이메일/비밀번호 검증 → 성공 시 Access + Refresh 토큰 발급, 실패 시 401 반환  
- **인증 요청** → Access Token 검증 → 유효 시 정상 응답, 만료 시 Refresh Token 확인 → 유효하면 새 Access Token 발급, 실패 시 401 반환  
- **로그아웃 (`/logout`)** → Refresh Token 블랙리스트 처리 후 로그아웃 완료
