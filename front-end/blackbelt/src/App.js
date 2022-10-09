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
import { UserContextProvider } from './lib/UserContext';

export default function App() {
  return (
    <ChakraProvider>
        {/* <UserContextProvider> */}
        <Router>
            <Routes>
            <Route path="/" element={<MainPage />} />
            </Routes>
        </Router>
        {/* </UserContextProvider> */}
    </ChakraProvider>
  );
}
