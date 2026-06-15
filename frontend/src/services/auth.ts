import { jwtDecode, type JwtPayload } from "jwt-decode";
import { api } from "./api";
import { setCookie } from "./cookies";

export async function createNewAccount() {
    let username = "Guest_" + Math.random().toString().substring(2, 15);

    try {
        const responseFromUserCreation = await api.post("user/create/", {
            username: username,
            password: username,
        });

        const responseFromTokenAcquisition = await api.post("user/token/", {
            username: username,
            password: username,
        });

        let userAccessData: JwtPayload & { username: string } = jwtDecode(
            responseFromTokenAcquisition.data.access,
        );
        username = userAccessData.username;
        setCookie("auth", JSON.stringify(responseFromTokenAcquisition.data));
        setCookie("username", username);
        return true;

    } catch (err: any) {
        console.log(err);
    }
    
    return false;
}