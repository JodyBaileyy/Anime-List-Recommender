import unittest

from unittest.mock import Mock, call, patch
from project import get_recommended_anime
from sql_queries import watch_list_query, add_anime_query

class TestGetRecommendedAnime(unittest.TestCase):
    def mocked_db(self, db_records=None):
        return Mock(execute=Mock(return_value=db_records), commit=Mock())
    
    def mocked_api_response():
        return [
            {"id": 10, "title": "Cowboy Bebop"},
            {"id": 20, "title": "ERASED"},
            {"id": 30, "title": "Naruto"}
        ]
    
    @patch("project.paginated_response", Mock(return_value=[]))
    @patch("builtins.print")
    def test_no_recommendations_found(self, mock_print):
        get_recommended_anime(db=self.mocked_db(), genres=[], min_score=20, max_episodes=20, formats=[], status="")
        
        mock_print.assert_called_with("No anime found with current options. Try narrowing down the criteria given")
        
    @patch("project.paginated_response", Mock(return_value=mocked_api_response()))
    @patch("builtins.print")
    def test_all_anime_included_in_watch_list(self, mock_print):
        mocked_db_anime = [
            (1, 'Cowboy Bebop', 10, None, 'PLAN TO WATCH'), 
            (2, 'ERASED', 20, None, 'PLAN TO WATCH'), 
            (3, "Naruto", 30, None, 'PLAN TO WATCH'),
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        
        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")
        
        db_mock.execute.assert_called_with(watch_list_query)
        mock_print.assert_called_with("All anime that match the given criteria are included in your watch list")
    
    @patch("project.paginated_response", Mock(return_value=mocked_api_response()))
    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("project.get_anime_title", Mock(return_value="ERASED"))
    @patch("builtins.input", Mock(return_value="y"))
    @patch("builtins.print")
    def test_add_recommended_anime_to_watch_list(self, mock_print):
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        
        
        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")
    
        db_mock.commit.assert_called()
        db_mock.execute.assert_has_calls([call(watch_list_query), call(add_anime_query, (20, "ERASED", None, "PLAN TO WATCH"))])
        mock_print.assert_has_calls([call("Formatted Anime Response"), call("Added ERASED to your watch list")])
        
    @patch("project.paginated_response", Mock(return_value=mocked_api_response()))
    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("builtins.input", Mock(return_value="n"))
    @patch("builtins.print")
    def test_reject_adding_recommended_anime_to_watch_list(self, mock_print):
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        
        
        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")
    
        db_mock.commit.assert_not_called()
        db_mock.execute.assert_has_calls([call(watch_list_query)])
        mock_print.assert_has_calls([call("Formatted Anime Response")])
        
    @patch("project.paginated_response", Mock(return_value=mocked_api_response()))
    @patch("project.get_random_anime", Mock(return_value={"id": 20, "title": "ERASED"}))
    @patch("project.formatted_recommended_anime", Mock(return_value="Formatted Anime Response"))
    @patch("project.get_anime_title", Mock(return_value="ERASED"))
    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_response_for_adding_recommended_anime_to_watch_list(self, mock_print, mock_input):
        mock_input.side_effect = ["invalid", "Still Invalid", "y"]
        invalid_message = "Invalid option given. Valid options: ['y', 'yes', 'n', 'no']"
        mocked_db_anime = [
            (4, "Demon Slayer", 40, None, 'PLAN TO WATCH')
        ]
        
        
        db_mock = self.mocked_db(mocked_db_anime)
        get_recommended_anime(db=db_mock, genres=[], min_score=20, max_episodes=20, formats=[], status="")
    
        db_mock.commit.assert_called()
        mock_input.call_count = 2
        db_mock.execute.assert_has_calls([call(watch_list_query), call(add_anime_query, (20, "ERASED", None, "PLAN TO WATCH"))])
        mock_print.assert_has_calls([call("Formatted Anime Response"), call(invalid_message), call(invalid_message), call("Added ERASED to your watch list")])
        
        
        
    
        
    

        
        
