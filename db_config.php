<?php

        $hostname = "localhost"; // 호스트명
        $username = "root"; // 데이터베이스 사용자명
        $password = "1234"; // 데이터베이스 비밀번호
        $dbname = "dataDB"; // 데이터베이스명

        // 데이터베이스 연결
        $mysqli = new mysqli($hostname, $username, $password, $dbname);

        // 연결 오류 발생 시 예외 처리
        if ($mysqli->connect_error) {
            die("데이터베이스 연결 실패: " . $mysqli->connect_error);
        }
    
    ?>