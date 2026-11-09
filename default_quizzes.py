from quiz import Quiz

DEFAULT_QUIZZES = [
    Quiz(
        "파이썬에서 함수를 정의할 때 사용하는 키워드는?",
        ["class", "def", "return", "import"],
        2,
        hint="영어로 정의하다는 define이에요.",
    ),
        Quiz(
        "파이썬에서 클래스를 정의할 때 사용하는 키워드는?",
        ["def", "import", "class", "return"],
        3,
        hint="Quiz와 QuizGame을 정의하는 줄의 맨 앞을 떠올려 보세요.",
    ),
        Quiz(
        "파이썬에서 화면에 글자를 출력할 때 사용하는 함수는?",
        ["input()", "len()", "int()", "print()"],
        4,
        hint="종이에 글자를 인쇄한다는 영어 단어를 떠올려 보세요.",
    ),
        Quiz(
        "파이썬에서 사용자 입력을 받는 함수는?",
        ["input()", "print()", "len()", "int()"],
        1,
        hint="메뉴에서 선택 번호를 기다릴 때 사용했던 함수예요.",
    ),
        Quiz(
        "파이썬 리스트에서 첫 번째 항목의 인덱스는?",
        ["1", "0", "2", "3"],
        2,
	    hint="리스트의 두 번째 항목은 리스트이름[1]로 꺼낼 수 있어요.",
    ),
]

