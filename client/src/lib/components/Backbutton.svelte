<script lang="ts">
import { browser } from "$app/environment";
import { goto } from "$app/navigation";
import { decrementNavigationCount, navigationCount } from "$lib/stores/navigation";

const getParentRoute = (path = globalThis.location.pathname) => {
	if (path.endsWith("/")) {
		path = path.slice(0, -1);
	}

	return path.slice(0, path.lastIndexOf("/")) || "/";
};

const goBack = () => {
	if (!browser) {
		return;
	}

	const currentNavigationCount = $navigationCount;

	if (currentNavigationCount > 1) {
		decrementNavigationCount(2);
		globalThis.history.back();
	} else {
		const parentRoute = getParentRoute();
		decrementNavigationCount();
		goto(parentRoute);
	}
};
</script>

<div class="mx-auto max-w-6xl px-4 pt-6 sm:px-6 lg:px-8">
	<button
		onclick={goBack}
		class="inline-flex items-center rounded-lg border border-gray-200 bg-white px-3.5 py-2 text-sm font-semibold text-gray-700 shadow-sm transition-colors hover:bg-gray-50 hover:text-gray-900 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
	>
		<svg class="mr-2 h-4 w-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
		</svg>
		Back
	</button>
</div>
