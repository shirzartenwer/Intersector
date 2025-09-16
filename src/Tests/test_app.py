from streamlit.testing.v1 import AppTest
import pytest

APP_PATH = "src/app.py"


def test_app_run_through_with_default_value():
    at = AppTest.from_file(APP_PATH)
    at.run()
    assert not at.exception


def test_app_display_default_values_correctly():
    at = AppTest.from_file(APP_PATH)
    at.run()
    assert at.number_input[0].value == 50
    assert at.number_input[1].value == 25   


@pytest.mark.parametrize("value", [0, 1000])
def test_the_add_sign_on_two_number_input_field(value):
    at = AppTest.from_file(APP_PATH).run()
    n_1 = at.number_input[0].set_value(value)
    n_2 = at.number_input[1].set_value(value)
    initial_value = n_1.value
    n_1.increment().run()
    n_2.increment().run()
    assert n_1.value == initial_value + 1
    assert n_2.value == initial_value + 1


@pytest.mark.parametrize("value", [1, 1000])
def test_the_minus_sign_on_two_number_input_field(value):
    at = AppTest.from_file(APP_PATH).run()
    n_1 = at.number_input[0].set_value(value)
    n_2 = at.number_input[1].set_value(value)
    initial_value = n_1.value
    n_1.decrement().run()
    n_2.decrement().run()
    assert n_1.value == initial_value - 1
    assert n_2.value == initial_value - 1


@pytest.mark.parametrize("size_a, size_b, choice", 
                         [(1000, 500, "Collection A"), 
                          (2000, 0, "Collection B"), 
                          (10, 5000, "Collection A")])
def test_give_other_values_to_number_and_choice_and_submit_then_it_runs(size_a, size_b, choice):
    at = AppTest.from_file(APP_PATH)
    at.run()
    at.number_input[0].set_value(size_a)
    at.number_input[1].set_value(size_b)
    at.radio(key="choice_given").set_value(choice)
    at.button(key="run_button").click().run()
    assert not at.exception


def test_when_no_option_is_chosen_then_no_choice_is_made():
    at = AppTest.from_file(APP_PATH).run()
    r = at.radio(key="choice_given")
    assert r.value is None  # initially nothing selected
    assert at.session_state["choice_given"] is None


@pytest.mark.parametrize("value", ["Collection A", "Collection B"])
def test_when_option_is_chosen_then_correct_choice_is_set(value):
    at = AppTest.from_file(APP_PATH).run()
    r = at.radio(key="choice_given")
    r.set_value(value).run()
    assert r.value == value
    assert r.index == (0 if value == "Collection A" else 1)
    assert at.session_state["choice_given"] == value


@pytest.mark.parametrize("value", ["Collection A", "Collection B"])
def test_when_option_is_chosen_and_submitted_shows_info_about_result_and_runtime(value):
    at = AppTest.from_file(APP_PATH).run()
    r = at.radio(key="choice_given")
    r.set_value(value).run()
    at.button(key="run_button").click().run()
    assert at.info[0].value.startswith("The size of the intersection is: ")
    assert at.info[1].value.startswith("The runtime of intersection was: ")



def test_when_no_option_is_chosen_and_submitted_shows_warning():
    at = AppTest.from_file(APP_PATH).run()
    at.button(key="run_button").click().run()
    assert "Please choose an option before submitting." == at.warning[0].value
    assert at.session_state["choice_given"] is None
    assert len(at.info) == 0




