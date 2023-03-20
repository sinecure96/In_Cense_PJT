import { Route, Routes } from "react-router";
import MainPage from "./pages/MainPage/MainPage";
import LogInPage from "./pages/LogInPage/LogInPage";
import SignUpPage from "./pages/SignUpPage/SignUpPage";
import ListPage from "./pages/ListPage/ListPage";
import DetailPage from "./pages/DetailPage/DetailPage";
import SharePage from "./pages/SharePage/SharePage";
import RegisterPage from "./pages/SharePage/RegisterPage";


function App() {
  return (
    <Routes>
      <Route index element={<MainPage />} />
      <Route path="/login" element={<LogInPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route path="/list" element={<ListPage />} />
      <Route path="/detail" element={<DetailPage />} />
      <Route path="/share" element={<SharePage />} />
      <Route path="/share/register" element={<RegisterPage />} />

    </Routes>
  );
}

export default App;
