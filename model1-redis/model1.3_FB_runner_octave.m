% Clear redis database
%system('/opt/homebrew/bin/redis-cli flushdb');

% Define the number of firms
number_of_firms = 10000; % You can modify this value to change the number of firms; eventually, this will need to reflect the 'Firm.count' parameter in model1.yaml

for i = 1:264 % 'howManyCycles' parameter in model1.yaml
    % Wait until Python has sent data
    while true
        [status, data] = system('/opt/homebrew/bin/redis-cli get python_to_octave');
        if status == 0 && !isempty(strtrim(data))
            break;
        endif
        pause(1); % Wait before checking again
    end

     % Process data
    printf("Octave received: %s\n", strtrim(data)); 
    
    % Clear the python_to_octave key to avoid stale reads
    system('/opt/homebrew/bin/redis-cli del python_to_octave');

    % Generate an array of number_of_firms random floats between 0 and 1
    rand_floats = rand(1, number_of_firms);

    % Convert arrays to strings
    float_str = sprintf('%f, ', rand_floats);

    % Remove the trailing comma and space
    float_str = float_str(1:end-2); 

    % Send result back to Redis
    index = strfind(data, sprintf("Python %d", i-1));
    index_start = strfind(data, "Start");
    if !isempty(index) || !isempty(index_start)
        % Prepare the result to send both arrays as a single string
        printf(sprintf('Octave computing step %s...', num2str(i)));
        pause(1); % Simulate processing time - demand code will go here
        result = sprintf('Step: %s, Floats: [%s]', num2str(i), float_str);
        printf(sprintf('Octave sending step %s\n', num2str(i)));
        redis_command = ['echo "', result, '" | /opt/homebrew/bin/redis-cli -x set octave_to_python'];
        system(redis_command);
    end

end
