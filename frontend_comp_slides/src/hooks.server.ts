import { authenticateUser } from "$lib"
import { redirect, type Handle } from "@sveltejs/kit"

export const handle: Handle = async ({ event, resolve }) => {
	const response = await resolve(event)
    
    // event.locals.user = authenticateUser(event)
    // let nonProtected = ['login', 'home']
    
	// if (nonProtected.includes(event.url.pathname)) {
    //     return response
		
	// } else {
        
        if (false) {
			throw redirect(303, "/login")
		}

    //     return response
    // }

    return response

}