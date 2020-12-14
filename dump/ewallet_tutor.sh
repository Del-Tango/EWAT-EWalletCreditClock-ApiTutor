#!/bin/bash -x

SERVER_ADDRESS='http://localhost:5000'
EWALLET_URI="$SERVER_ADDRESS/ewallet"
INSTRUCTION_SET_URI="$EWALLET_URI/instruction-set"

function display_user_action_request_client_id () {
    HTTP_REQUEST=`curl -i -H "Content-Type: application/json" -X GET \
        -d '{"option": "action", "action": "RequestClientID"}' \
        $INSTRUCTION_SET_URI`
    echo $HTTP_REQUEST | python -m json.tool
}

function handle_display_user_action () {
    AVAILABLE_ACTIONS=`curl -i -H "Content-Type: application/json" -X GET \
        -d '{}' $INSTRUCTION_SET_URI`
        echo $HTTP_REQUEST | python3 -m json.loads
    read -p 'Action> ' ACTION
    case "$ACTION" in
        'RequestClientID')
            display_user_action_request_client_id
            ;;
    esac
    return 0
}

function handle_display_user_event () {
    pass
}

function main_menu () {
    OPTIONS=( 'Select-User-Action' 'Select-User-Event' 'Exit-Tutor' )
    select opt in "${OPTIONS[@]}"; do
        case "$opt" in
            'Select-User-Action')
                handle_display_user_action
                break
                ;;
            'Select-User-Event')
                handle_display_user_event
                break
                ;;
            'Exit-Tutor')
                exit 0
                ;;
            *)
                warning "Invalid EWallet Credit Clock api tutor option $opt."
                ;;
        esac
    done
    return 0
}

function ewallet_credit_clock_api_tutor_init () {
    while :
    do
        main_menu
        EXIT_CODE=$?
        if [ $EXIT_CODE -ne 0 ]; then
            exit $EXIT_CODE
        fi
    done
}

function warning () {
    MSG="$@"
    echo "[ WARNING ]: $MSG"
    return 1
}

ewallet_credit_clock_api_tutor_init

# CODE DUMP

#vcurl -i -H "Content-Type: application/json" -X GET -d '{"option": "action", "action": "ViewAccount"}' http://localhost:5000/ewallet
