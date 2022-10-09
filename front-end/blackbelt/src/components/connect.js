import {Button, Box, Text, Center } from "@chakra-ui/react"

export default function ConnectWalletButton() {
    return (<Center>
        <Button colorScheme='purple' type='submit' className="connectButton">
            Add to MetaMask Snap
        </Button>
        </Center>
    )
}