import random
import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from default_quizzes import DEFAULT_QUIZZES
from quiz import Quiz

class QuizGame:
    def __init__(self):
        self.quizzes = DEFAULT_QUIZZES.copy()
        self.best_score = None
        self.history = []
        self._last_saved_text = None
        self.load_state()

    def show_menu(self):
        print("\n=== 나만의 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 점수 히스토리")
        print("7. 종료")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0
        score = 0

        available = len(self.quizzes)
        question_count = read_number(f"몇 문제를 풀까요? (1~{available}): ", 1, available)
        round_quizzes = random.sample(self.quizzes, question_count)

        for number, quiz in enumerate(round_quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()
            answer, hint_used = read_quiz_answer(quiz)

            if quiz.is_correct(answer):
                correct_count += 1
                if hint_used:
                    print("정답입니다! 힌트를 사용해서 이 문제는 0점입니다.")
                else:
                    score += 1
                    print("정답입니다!")
            else:
                print("오답입니다.")

        total = len(round_quizzes)
        print(f"\n결과: {total}문제 중 {correct_count}문제 정답 ({score}점)")
        self.history.append({
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "question_count": total,
            "score": score,
        })

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 기록입니다!")

        self.save_state()

    def add_quiz(self):
        while True:
            question = input("새 문제를 입력하세요: ").strip()

            if question:
                break

            print("문제를 한 글자 이상 입력하세요.")

        choices = []

        for number in range(1, 5):
            while True:
                choice = input(f"선택지 {number}: ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("선택지를 한 글자 이상 입력하세요.")

        answer = read_answer()
        quiz = Quiz(question, choices, answer)

        self.quizzes.append(quiz)
        self.save_state()
        print("퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"{number}. {quiz.question}")

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        number = read_number(
            "삭제할 문제 번호를 입력하세요 (0은 취소): ",
            0,
            len(self.quizzes),
        )

        if number == 0:
            print("삭제를 취소했습니다.")
            return

        removed_quiz = self.quizzes.pop(number - 1)
        self.save_state()
        print(f"삭제한 문제: {removed_quiz.question}")
        print("퀴즈가 삭제되었습니다.")

    def show_best_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"최고 기록: {self.best_score}점")

    def show_history(self):
        if not self.history:
            print("아직 플레이 기록이 없습니다.")
            return

        print("\n=== 점수 히스토리 (최근 기록부터) ===")
        for record in reversed(self.history):
            played_at = datetime.fromisoformat(record["played_at"])
            date_text = played_at.strftime("%Y-%m-%d %H:%M:%S")
            question_count = record["question_count"]
            score = record["score"]
            print(f"{date_text} | 푼 문제 {question_count}개 | {score}점")

    def save_state(self):
        quiz_data = []

        for quiz in self.quizzes:
            quiz_data.append({
                "question": quiz.question,
                "choices": quiz.choices,
                "answer": quiz.answer,
                "hint": quiz.hint,
            })

        state = {
            "quizzes": quiz_data,
            "best_score": self.best_score,
            "history": self.history,
        }

        state_path = Path(__file__).resolve().with_name("state.json")

        try:
            state_text = json.dumps(state, ensure_ascii=False, indent=4)

            with TemporaryDirectory(prefix=".state-", dir=state_path.parent) as temp_dir:
                temp_path = Path(temp_dir) / "state.json"

                with temp_path.open("w", encoding="utf-8") as file:
                    file.write(state_text)
                    file.flush()
                    os.fsync(file.fileno())

                if self._last_saved_text is not None:
                    backup_path = state_path.with_name("state.json.bak")
                    temp_backup_path = Path(temp_dir) / "state.json.bak"

                    with temp_backup_path.open("w", encoding="utf-8") as file:
                        file.write(self._last_saved_text)
                        file.flush()
                        os.fsync(file.fileno())

                    temp_backup_path.replace(backup_path)

                temp_path.replace(state_path)
                self._last_saved_text = state_text
        except OSError as error:
            print(f"저장하지 못했습니다. {error}")

    def load_state(self):
        state_path = Path(__file__).resolve().with_name("state.json")
        original_loaded = self._load_state_file(state_path)
        if original_loaded:
            return

        backup_path = state_path.with_name("state.json.bak")
        backup_loaded = self._load_state_file(backup_path)
        if backup_loaded:
            print("원본 저장 파일을 불러올 수 없어 백업에서 시작합니다.")
        elif original_loaded is False or backup_loaded is False:
            print("저장 파일을 불러올 수 없어 기본 문제로 시작합니다.")

    def _load_state_file(self, state_path):

        try:
            with state_path.open("r", encoding="utf-8") as file:
                saved_text = file.read()
                state = json.loads(saved_text)

            quiz_items = state["quizzes"]
            if not isinstance(quiz_items, list):
                raise ValueError("퀴즈 목록은 리스트여야 합니다.")

            quizzes = []
            hints_added = False
            for item in quiz_items:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제 문장이 비어 있거나 잘못되었습니다.")

                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("선택지는 4개여야 합니다.")

                for choice in choices:
                    if not isinstance(choice, str) or not choice.strip():
                        raise ValueError("선택지는 비어 있지 않은 문자열이어야 합니다.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

                hint = item.get("hint")
                if hint is not None and not isinstance(hint, str):
                    raise ValueError("힌트는 문자열이어야 합니다.")

                if "hint" not in item:
                    for default_quiz in DEFAULT_QUIZZES:
                        if (
                            question == default_quiz.question
                            and choices == default_quiz.choices
                            and answer == default_quiz.answer
                        ):
                            hint = default_quiz.hint
                            if hint is not None:
                                hints_added = True
                            break

                quizzes.append(Quiz(question, choices, answer, hint=hint))

            best_score = state["best_score"]

            if best_score is not None:
                if type(best_score) is not int or best_score < 0:
                    raise ValueError("최고 점수는 0 이상의 정수여야 합니다.")
            history = state.get("history", [])
            if not isinstance(history, list):
                raise ValueError("플레이 기록은 리스트여야 합니다.")

            for record in history:
                datetime.fromisoformat(record["played_at"])
                question_count = record["question_count"]
                score = record["score"]

                if type(question_count) is not int or question_count < 1:
                    raise ValueError("푼 문제 수는 1 이상의 정수여야 합니다.")

                if type(score) is not int or not 0 <= score <= question_count:
                    raise ValueError("점수는 0부터 푼 문제 수 사이여야 합니다.")
                                
        except FileNotFoundError:
            return None
        except (OSError, ValueError, KeyError, TypeError):
            return False

        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history
        self._last_saved_text = saved_text

        if hints_added and state_path.name == "state.json":
            self.save_state()

        return True

def read_number(prompt, minimum, maximum):
    while True:
        text = input(prompt).strip()

        try:
            number = int(text)
        except ValueError:
            print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")


def read_answer():
    return read_number("정답 번호 (1~4): ", 1, 4)

def read_quiz_answer(quiz):
    hint_used = False
    while True:
        text = input("정답 번호 (1~4, 힌트는 h): ").strip().lower()

        if text == "h":
            if quiz.hint:
                print(f"힌트: {quiz.hint}")
                hint_used = True
            else:
                print("이 문제에는 힌트가 없습니다.")
            continue

        try:
            answer = int(text)
        except ValueError:
            print("1~4 사이의 숫자 또는 h를 입력하세요.")
            continue

        if 1 <= answer <= 4:
            return answer, hint_used

        print("1~4 사이의 숫자 또는 h를 입력하세요.")

def main():
    game = QuizGame()
    
    while True:
        game.show_menu()
        choice = input("선택: ").strip()

        if choice == "7":
            print("게임을 종료합니다.")
            break
        
        elif choice == "1":
            game.play_quiz()
        elif choice == "2":
            game.add_quiz()
        elif choice == "3":
            game.show_quiz_list()
        elif choice == "4":
            game.show_best_score()
        elif choice == "5":
            game.delete_quiz()
        elif choice == "6":
            game.show_history()
        else:
            print("1~7 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n게임을 종료합니다.")