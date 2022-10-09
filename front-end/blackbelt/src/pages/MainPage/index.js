import {
    Box,
    Text,
    Link,
    VStack,
    Code,
    Grid,
  } from '@chakra-ui/react';
import { ColorModeSwitcher } from '../../ColorModeSwitcher';
import { Logo } from '../../Logo';
import { SimpleCard } from '../../components/form'
import { Results } from '../../components/results'

export function MainPage() {
    return (
        <Box textAlign="center" fontSize="xl">
        <SimpleCard id = "form"/>
        <Results id = "result"/>
        </Box>
    )
}

