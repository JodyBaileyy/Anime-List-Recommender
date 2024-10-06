import unittest

from unittest.mock import Mock, call, patch
from project import get_recommended_anime, view_watch_list, add_anime_to_watch_list, update_anime_in_watch_list, delete_anime_in_watch_list
from sql_queries import watch_list_query, add_anime_query, update_query, delete_query
from constants import (
    INVALID_OPTION_MSG,
    INVALID_CONFIRMATION_MSG,
    WATCH_LIST_EMPTY_MSG,
    INVALID_PROPERTIES_MSG,
    INVALID_SCORE_MSG,
    INVALID_STATUS_MSG,
    NO_RECOMMENDATIONS_FOUND_MSG,
    NO_UNIQUE_RECOMMENDATION_FOUND_MSG,
    CANCEL_DELETE_MSG
)


class BaseWatchListTest(unittest.TestCase):
    def mocked_db(self, db_records=None):
        return Mock(execute=Mock(return_value=db_records), commit=Mock())

    def mocked_api_response(self):
        return [
            {
                "id": 10,
                "title": {
                    "english": "Cowboy Bebop",
                    "userPreffered": "Cowboy Bebop"
                },
                "format": "TV",
                "averageScore": 86,
                "episodes": 26,
                "startDate": {
                    "year": 1998
                },
                "season": "SPRING",
                "studios": {
                    "edges": [
                        {
                            "node": {
                                "name": "Sunrise"
                            }
                        }
                    ]
                }
            },
            {
                "id": 20,
                "title": {
                    "english": "ERASED",
                    "userPreffered": "ERASED"
                },
                "format": "TV",
                "averageScore": 78,
                "episodes": 12,
                "startDate": {
                    "year": 2016
                },
                "season": "WINTER",
                "studios": {
                    "edges": [
                        {
                            "node": {
                                "name": "A-1 Pictures"
                            }
                        }
                    ]
                }
            },
            {
                "id": 30,
                "title": {
                    "english": "Naruto",
                    "userPreffered": "Naruto"
                },
                "format": "TV",
                "averageScore": 78,
                "episodes": 220,
                "startDate": {
                    "year": 2002
                },
                "season": "FALL",
                "studios": {
                    "edges": [
                        {
                            "node": {
                                "name": "Studio Pierrot"
                            }
                        }
                    ]
                }
            }
        ]


class TestGetRecommendedAnime(BaseWatchListTest):
    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("project.get_anime_title", Mock(return_value="ERASED"))
    @patch("builtins.input", Mock(return_value="y"))
    @patch("project.paginated_response")
    @patch("builtins.print")
    def test_add_recommended_anime_to_watch_list(self, mock_print, mock_response):
        """
        Test the happy path for when a recommendation is provided
        and the user adds the anime to their watch list
        """
        mock_response.return_value = self.mocked_api_response()
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(
            db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")

        db_mock.commit.assert_called_once()
        db_mock.execute.assert_has_calls([call(watch_list_query), call(
            add_anime_query, (20, "ERASED", None, "PLAN TO WATCH"))])
        mock_print.assert_has_calls(
            [call("Formatted Anime Response"), call("Added ERASED to your watch list")])

    @patch("project.paginated_response")
    @patch("builtins.print")
    def test_no_recommendation_found(self, mock_print, mock_response):
        """Test when no recommendation is found with the provided criteria"""

        mock_response.return_value = []
        db_mock = self.mocked_db(())

        get_recommended_anime(
            db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")

        db_mock.execute.assert_not_called()
        mock_print.assert_called_with(NO_RECOMMENDATIONS_FOUND_MSG)

    @patch("project.paginated_response")
    @patch("builtins.print")
    def test_all_anime_included_in_watch_list(self, mock_print, mock_response):
        """
        Test when all recommended anime that is given
        is already included in the user's watch list 
        """
        mock_response.return_value = self.mocked_api_response()
        mocked_db_anime = [
            (1, 'Cowboy Bebop', 10, None, 'PLAN TO WATCH'),
            (2, 'ERASED', 20, None, 'PLAN TO WATCH'),
            (3, "Naruto", 30, None, 'PLAN TO WATCH'),
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(
            db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")

        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_with(NO_UNIQUE_RECOMMENDATION_FOUND_MSG)

    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("builtins.input", Mock(return_value="n"))
    @patch("project.paginated_response")
    @patch("builtins.print")
    def test_reject_adding_recommended_anime_to_watch_list(self, mock_print, mock_response):
        """
        Test when a recommended anime is provided,
        but the user decides to not add it to their watch list
        """
        mock_response.return_value = self.mocked_api_response()
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(
            db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")

        db_mock.commit.assert_not_called()
        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_has_calls([call("Formatted Anime Response")])

    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("project.get_anime_title", Mock(return_value="ERASED"))
    @patch("project.paginated_response")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_response_for_adding_recommended_anime_to_watch_list(self, mock_print, mock_input, mock_response):
        """
        Test when a recommendation is provided,
        but the user gives an invalid option when trying to add it to their watch list
        """
        mock_response.return_value = self.mocked_api_response()
        mock_input.side_effect = ["invalid", "Still Invalid", "y"]
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(
            db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")

        mock_input.call_count = 2
        db_mock.commit.assert_called()
        db_mock.execute.assert_has_calls([call(watch_list_query), call(
            add_anime_query, (20, "ERASED", None, "PLAN TO WATCH"))])
        mock_print.assert_has_calls([call("Formatted Anime Response"), call(
            INVALID_CONFIRMATION_MSG), call(INVALID_CONFIRMATION_MSG), call("Added ERASED to your watch list")])

    @patch("project.paginated_response", Mock(return_value=[]))
    @patch("builtins.print")
    def test_no_recommendations_found(self, mock_print):
        """Test when no recommendation is provided"""
        get_recommended_anime(db=self.mocked_db(), genres=[],
                              min_score=20, max_episodes=20, formats=[], status="")

        mock_print.assert_called_with(
            "No anime found with current options. Try narrowing down the criteria given")


class ViewWatchList(BaseWatchListTest):
    @patch("project.format_record_for_watch_list")
    @patch("project.get_single_anime")
    @patch("project.tabulate")
    @patch("builtins.print")
    def test_view_watch_list(self, mock_print, mock_tabulate, mock_single_anime, mock_formattted_record):
        """Test viewing the entries in the user's watch list"""
        mocked_db_anime = [
            (1, 'Cowboy Bebop', 10, None, 'PLAN TO WATCH'),
            (2, 'ERASED', 20, None, 'PLAN TO WATCH'),
            (3, "Naruto", 30, None, 'PLAN TO WATCH'),
        ]
        mock_formatted_records = [f"Formatted record for {
            record[1]}" for record in mocked_db_anime]

        mock_single_anime.side_effect = self.mocked_api_response()
        mock_formattted_record.side_effect = mock_formatted_records
        db_mock = self.mocked_db(mocked_db_anime)

        view_watch_list(db_mock)

        assert mock_formatted_records in mock_tabulate.call_args.args
        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_with(mock_tabulate())

    @patch("builtins.print")
    def test_watch_list_empty(self, mock_print):
        """Test when there are no entries in the watch list"""
        db_mock = self.mocked_db(())

        view_watch_list(db_mock)

        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_with(WATCH_LIST_EMPTY_MSG)


class AddToWatchList(BaseWatchListTest):
    @patch("project.tabulate")
    @patch("project.format_response_for_add")
    @patch("project.paginated_response")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_happy_path(self, mock_input, mock_print, mock_paginated_response, mock_formatted_response, mock_tabulate):
        """Testing the path where api responses are received and the expected input is given"""
        db_mock = self.mocked_db(())
        mock_formatted_records = [f"Formatted record for {
            record["title"]}" for record in self.mocked_api_response()]

        mock_input.side_effect = ["Cowboy Bebop", "1", "completed", "86"]
        mock_paginated_response.return_value = self.mocked_api_response()
        mock_formatted_response.side_effect = mock_formatted_records

        add_anime_to_watch_list(db_mock)

        assert mock_input.call_count == 4
        assert mock_formatted_records in mock_tabulate.call_args.args
        mock_print.assert_has_calls([
            call(mock_tabulate(), end="\n\n"),
            call(),
            call("Added Cowboy Bebop to watch list")
        ])
        db_mock.execute.assert_called_with(
            add_anime_query, (10, "Cowboy Bebop", 86, "COMPLETED"))
        db_mock.commit.assert_called_once()

    @patch("project.tabulate")
    @patch("project.format_response_for_add")
    @patch("project.paginated_response")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_dreaded_path(self, mock_input, mock_print, mock_paginated_response, mock_formatted_response, mock_tabulate):
        """
        Testing the path where multiple api requests are required 
        and all instances of unexpected input are caught and handled
        """

        db_mock = self.mocked_db(())
        mock_formatted_records = [f"Formatted record for {
            record["title"]}" for record in self.mocked_api_response()]

        mock_input.side_effect = [
            "Unknown Anime",
            "Cowboy Bebop",
            "Invalid Option",
            "50",
            "1",
            "Invalid Status",
            "plan to watch",
            "Invalid Score",
            "101",
            EOFError,
        ]
        mock_paginated_response.side_effect = [[], self.mocked_api_response()]
        mock_formatted_response.side_effect = mock_formatted_records

        add_anime_to_watch_list(db_mock)

        assert mock_input.call_count == 10
        assert mock_formatted_records in mock_tabulate.call_args.args
        mock_print.assert_has_calls([
            call("No anime found with name Unknown Anime"),
            call(mock_tabulate(), end="\n\n"),
            call(INVALID_OPTION_MSG),
            call(INVALID_OPTION_MSG),
            call(INVALID_STATUS_MSG),
            call(INVALID_SCORE_MSG),
            call(INVALID_SCORE_MSG),
            call(),
            call("Added Cowboy Bebop to watch list")
        ])
        db_mock.execute.assert_called_with(
            add_anime_query, (10, "Cowboy Bebop", None, "PLAN TO WATCH"))
        db_mock.commit.assert_called_once()


class UpdateEntryInWatchList(BaseWatchListTest):
    @patch("helpers.table_record_for_viewing")
    @patch("helpers.tabulate")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_happy_path(self, mock_input, mock_print, mock_tabulate, mock_table_record):
        """
        Testing the path where the expected input is given,
        resulting in the entry in the watch list being updated
        """

        mocked_db_anime = [
            (1, 'Cowboy Bebop', 10, None, 'PLAN TO WATCH'),
            (2, 'ERASED', 20, None, 'PLAN TO WATCH'),
            (3, "Naruto", 30, None, 'PLAN TO WATCH'),
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        mock_table_record.side_effect = mocked_db_anime
        mock_input.side_effect = ["2", "score", "70"]
        db_mock = self.mocked_db(mocked_db_anime)

        update_anime_in_watch_list(db_mock)

        assert mocked_db_anime in mock_tabulate.call_args.args
        db_mock.commit.assert_called_once()
        db_mock.execute.assert_called_with(
            update_query.format(column="score"),
            (70, 2)
        )
        mock_print.assert_has_calls([
            call(mock_tabulate(), end='\n\n'),
            call(),
            call("Successfully updated ERASED's score to 70")
        ])

    @patch("helpers.table_record_for_viewing")
    @patch("helpers.tabulate")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_dreaded_path(self, mock_input, mock_print, mock_tabulate, mock_table_record):
        """
        Testing the path where unexpected input is provided,
        but the entry is ultimately updated
        """

        mocked_db_anime = [
            (1, 'Cowboy Bebop', 10, None, 'PLAN TO WATCH'),
            (2, 'ERASED', 20, None, 'PLAN TO WATCH'),
            (3, "Naruto", 30, None, 'PLAN TO WATCH'),
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]

        mock_table_record.side_effect = mocked_db_anime
        mock_input.side_effect = [
            "Invalid Option",
            "23",
            "1",
            "Invalid Property",
            "status",
            "Invalid Status",
            "Completed",
        ]
        db_mock = self.mocked_db(mocked_db_anime)

        update_anime_in_watch_list(db_mock)

        assert mock_input.call_count == 7
        assert mocked_db_anime in mock_tabulate.call_args.args
        db_mock.commit.assert_called_once()
        db_mock.execute.assert_called_with(
            update_query.format(column="status"),
            ("COMPLETED", 1)
        )
        mock_print.assert_has_calls([
            call(mock_tabulate(), end='\n\n'),
            call(INVALID_OPTION_MSG),
            call(INVALID_OPTION_MSG),
            call(INVALID_PROPERTIES_MSG),
            call(INVALID_STATUS_MSG),
            call(),
            call("Successfully updated Cowboy Bebop's status to COMPLETED")
        ])

    @patch("builtins.print")
    def test_no_entries_to_update(self, mock_print):
        """
        Test when the user tries to update an entry in their watch list,
        but their watch list is currently empty
        """
        db_mock = self.mocked_db(())

        update_anime_in_watch_list(db_mock)

        db_mock.commit.assert_not_called()
        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_once_with(WATCH_LIST_EMPTY_MSG)


class DeleteEntryInWatchList(BaseWatchListTest):
    @patch("helpers.table_record_for_viewing")
    @patch("helpers.tabulate")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_happy_path(self, mock_input, mock_print, mock_tabulate, mock_table_record):
        """
        Test when the expected input is given for each step,
        resulting in the entry being deleted from the watch lists
        """
        mocked_db_anime = [
            (1, "Naruto", 30, None, 'PLAN TO WATCH'),
            (2, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        db_mock = self.mocked_db(mocked_db_anime)

        mock_input.side_effect = ["2", "y"]
        mock_table_record.side_effect = mocked_db_anime

        delete_anime_in_watch_list(db_mock)

        assert mocked_db_anime in mock_tabulate.call_args.args
        db_mock.execute.assert_has_calls([
            call(watch_list_query),
            call(delete_query, (2,))
        ])
        db_mock.commit.assert_called_once()
        mock_print.assert_has_calls([
            call(mock_tabulate(), end="\n\n"),
            call("Successfully deleted Demon Slayer from your watch list")
        ])

    @patch("helpers.table_record_for_viewing")
    @patch("helpers.tabulate")
    @patch("builtins.print")
    @patch("builtins.input")
    def test_dreaded_path(self, mock_input, mock_print, mock_tabulate, mock_table_record):
        """
        Test when invalid input is given when trying to delete a record in the user's watch list,
        and when the user ultimately decides not to delete the entry
        """
        mocked_db_anime = [
            (1, "Naruto", 30, None, 'PLAN TO WATCH'),
            (2, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        db_mock = self.mocked_db(mocked_db_anime)

        mock_input.side_effect = [
            "Invalid Number",
            "20",
            "2",
            "nope",
            "n"
        ]
        mock_table_record.side_effect = mocked_db_anime

        delete_anime_in_watch_list(db_mock)

        assert mocked_db_anime in mock_tabulate.call_args.args
        assert mock_input.call_count == 5
        db_mock.execute.assert_called_once_with(watch_list_query)
        db_mock.commit.assert_not_called()
        mock_print.assert_has_calls([
            call(mock_tabulate(), end="\n\n"),
            call(INVALID_OPTION_MSG),
            call(INVALID_OPTION_MSG),
            call(INVALID_CONFIRMATION_MSG),
            call(CANCEL_DELETE_MSG)
        ])

    @patch("builtins.print")
    def test_no_entries_to_delete(self, mock_print):
        """
        Test when a user tries to delete an entry in their watch list,
        but their watch list is currently empty
        """
        db_mock = self.mocked_db(())

        delete_anime_in_watch_list(db_mock)

        db_mock.commit.assert_not_called()
        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_once_with(WATCH_LIST_EMPTY_MSG)
