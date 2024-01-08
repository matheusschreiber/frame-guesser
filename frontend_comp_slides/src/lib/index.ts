import { redirect, type RequestEvent } from "@sveltejs/kit"
import { getCookie } from "../services/cookies"

export const authenticateUser = () => {
	const rawCookie = getCookie("auth") // FIXME: nao tem document.cookie em SSR
	if (!rawCookie) return false
	return JSON.parse(rawCookie).access
}