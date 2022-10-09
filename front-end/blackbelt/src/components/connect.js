import {Button, Box, Text, Center, Link} from "@chakra-ui/react"

export default function ConnectWalletButton() {
    return (<Center>
         <a href="http://localhost:3000/">
         <Button colorScheme='purple' type='submit' className="connectButton">
            Add to MetaMask Snap
        </Button>
        </a>
        </Center>
    )
}