import * as React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import {
  ChakraProvider,
} from '@chakra-ui/react';
import { MainPage } from "./pages";
import { Nav } from "./components/nav";

export default function App() {
  return (
    <ChakraProvider>        
        <Router>
        <Nav/>
            <Routes>
            <Route path="/" element={<MainPage />} />
            </Routes>
        </Router>
    </ChakraProvider>
  );
}
