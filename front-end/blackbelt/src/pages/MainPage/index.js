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
        {/* // <Grid minH="100vh" p={3}>
        // <ColorModeSwitcher justifySelf="flex-end" />
        // <VStack spacing={8}>
        //     <Logo h="40vmin" pointerEvents="none" />
        //     <Text>
        //     Edit <Code fontSize="xl">src/App.js</Code> and save to reload.
        //     </Text>
        //     <Link */
        //     color="teal.500"
        //     href="https://chakra-ui.com"
        //     fontSize="2xl"
        //     target="_blank"
        //     rel="noopener noreferrer"
        //     >
        //     Learn Chakra
        //     </Link>
        // </VStack>
        // </Grid>
    }
        <SimpleCard id = "form"/>
        <Results id = "result"/>
        </Box>
    )
}

