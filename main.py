"""
Main entry point for the Automated Candidate Screening Workflow.
"""

import sys
import argparse
from pathlib import Path
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from workflow.orchestrator import WorkflowOrchestrator


def setup_logging():
    """Configure logging for the application."""
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file logger
    logger.add(
        settings.log_file,
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    logger.info("Logging configured successfully")


def run_workflow():
    """Run the main workflow continuously."""
    logger.info("Starting Automated Candidate Screening Workflow")
    logger.info(f"Configuration: {settings.dict()}")
    
    orchestrator = WorkflowOrchestrator()
    
    # Test connections before starting
    logger.info("Testing service connections...")
    connection_results = orchestrator.test_connections()
    
    for service, status in connection_results.items():
        if status:
            logger.info(f"✓ {service} connection successful")
        else:
            logger.error(f"✗ {service} connection failed")
    
    if not all(connection_results.values()):
        logger.error("Some service connections failed. Please check configuration.")
        return False
    
    logger.info("All connections successful. Starting workflow...")
    
    try:
        orchestrator.run_continuous()
    except KeyboardInterrupt:
        logger.info("Workflow stopped by user")
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        return False
    
    return True


def run_single_cycle():
    """Run a single processing cycle."""
    logger.info("Running single cycle of candidate screening")
    
    orchestrator = WorkflowOrchestrator()
    cycle_stats = orchestrator.run_single_cycle()
    
    logger.info("Single cycle completed")
    logger.info(f"Results: {cycle_stats}")
    
    return cycle_stats


def test_workflow():
    """Test the workflow with sample data."""
    logger.info("Testing workflow with sample data")
    
    orchestrator = WorkflowOrchestrator()
    
    # Test data
    test_data = {
        'sender_email': 'john.doe@example.com',
        'sender_name': 'John Doe',
        'subject': 'Application for Python Developer Position',
        'body': '''
        Dear Hiring Team,
        
        I am writing to apply for the Python Developer position at your company.
        I have 4 years of experience as a Mid-level developer working with Python
        and have recently been exploring GenAI technologies.
        
        Please find my resume attached.
        
        Best regards,
        John Doe
        '''
    }
    
    result = orchestrator.process_test_email(test_data)
    
    logger.info("Test Results:")
    logger.info(f"Candidate: {result['candidate']}")
    logger.info(f"Email Response Subject: {result['email_response']['subject']}")
    logger.info(f"Screening Summary: {result['screening_summary']}")
    
    return result


def show_status():
    """Show current workflow status."""
    logger.info("Retrieving workflow status")
    
    orchestrator = WorkflowOrchestrator()
    status = orchestrator.get_status()
    
    print("\n=== Workflow Status ===")
    print(f"Total Processed: {status['workflow_stats']['total_processed']}")
    print(f"Matched Candidates: {status['workflow_stats']['matched_candidates']}")
    print(f"Rejected Candidates: {status['workflow_stats']['rejected_candidates']}")
    print(f"Emails Sent: {status['workflow_stats']['emails_sent']}")
    print(f"Errors: {status['workflow_stats']['errors']}")
    
    print(f"\n=== Sheet Statistics ===")
    for key, value in status['sheet_stats'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print(f"\n=== Configuration ===")
    print(f"Check Interval: {status['settings']['check_interval']} seconds")
    print(f"Max Emails Per Run: {status['settings']['max_emails_per_run']}")
    print(f"Required Keywords: {', '.join(status['settings']['required_keywords'])}")
    print(f"Minimum Matches: {status['settings']['minimum_keyword_matches']}")
    
    return status


def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Automated Candidate Screening Workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run                 # Run continuous workflow
  python main.py single              # Run single cycle
  python main.py test                # Test with sample data
  python main.py status              # Show current status
        """
    )
    
    parser.add_argument(
        'command',
        choices=['run', 'single', 'test', 'status'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default=settings.log_level,
        help='Set logging level'
    )
    
    args = parser.parse_args()
    
    # Override log level if specified
    if args.log_level != settings.log_level:
        settings.log_level = args.log_level
    
    # Setup logging
    setup_logging()
    
    # Execute command
    try:
        if args.command == 'run':
            success = run_workflow()
            sys.exit(0 if success else 1)
        
        elif args.command == 'single':
            run_single_cycle()
        
        elif args.command == 'test':
            test_workflow()
        
        elif args.command == 'status':
            show_status()
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()