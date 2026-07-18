<script lang="ts">
import type { User } from "$lib/types";

interface Props {
	user: User;
}

const { user }: Props = $props();
</script>

<a href="/persons/{user.id}">
	<div
		class="flex w-full cursor-pointer items-center space-x-3 rounded-lg border border-gray-200 bg-white p-3 text-left shadow-sm transition-shadow hover:shadow-md"
	>
		<div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-lg font-medium text-blue-600">
			{user.name.charAt(0).toUpperCase()}
		</div>
		<div>
			<p class="text-sm font-medium text-gray-900">{user.name}</p>
		</div>
	</div>
</a>
