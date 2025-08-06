<script lang="ts">
	import { goto } from '$app/navigation';

	const goBack = () => {
		// Check if there's history and if the previous page is on the same origin
		if (document.referrer && new URL(document.referrer).origin === window.location.origin) {
			window.history.back();
		} else {
			// Navigate to parent page based on current path
			const currentPath = window.location.pathname;

			if (currentPath.startsWith('/competitions/') && currentPath !== '/competitions') {
				goto('/competitions');
			} else if (currentPath.startsWith('/dashboard/')) {
				if (currentPath === '/dashboard' || currentPath === '/dashboard/') {
					goto('/');
				} else {
					goto('/dashboard');
				}
			} else if (currentPath.startsWith('/records')) {
				goto('/');
			} else if (currentPath.startsWith('/rankings')) {
				goto('/');
			} else {
				// Default fallback to home
				goto('/');
			}
		}
	};
</script>

<div class="ms-2 mt-2">
	<button
		onclick={goBack}
		class="inline-flex items-center rounded-md bg-gray-600 py-2 pe-4 ps-3 text-sm font-medium text-white transition-colors duration-150 hover:bg-gray-700"
	>
		<svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
		</svg>
		Back
	</button>
</div>
